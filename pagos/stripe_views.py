# stripe_views.py
import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Tarjeta

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_setup_intent(request):
    user = request.user

    # Crear o recuperar Customer en Stripe
    stripe_customer_id = getattr(user, "stripe_customer_id", None)
    if not stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.nombre  # usa 'nombre' en lugar de 'username'
        )
        stripe_customer_id = customer["id"]
        user.stripe_customer_id = stripe_customer_id
        user.save()

    # Crear SetupIntent para almacenar la tarjeta de forma segura
    intent = stripe.SetupIntent.create(customer=stripe_customer_id, usage="off_session")
    return Response({"client_secret": intent.client_secret})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def attach_payment_method(request):
    user = request.user
    pm_id = request.data.get("payment_method_id")
    if not pm_id:
        return Response({"detail": "payment_method_id required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Adjuntar PaymentMethod al Customer
        pm = stripe.PaymentMethod.attach(pm_id, customer=user.stripe_customer_id)

        # Comprobar si existe ya una tarjeta por defecto
        if not Tarjeta.objects.filter(usuario=user, default=True).exists():
            is_default = True
        else:
            is_default = False

        # Crear tarjeta en la base de datos
        card = pm.card
        tarjeta = Tarjeta.objects.create(
            usuario=user,
            nombre_titular=pm.billing_details.name or user.nombre,
            numero_enmascarado=f"**** **** **** {card.last4}",
            exp_mes=card.exp_month,
            exp_ano=card.exp_year,
            token=pm_id,
            default=is_default
        )

        # Establecer en Stripe como método de pago por defecto solo si es la primera
        if is_default:
            stripe.Customer.modify(
                user.stripe_customer_id,
                invoice_settings={"default_payment_method": pm_id}
            )

        return Response({
            "id": tarjeta.id,
            "nombre_titular": tarjeta.nombre_titular,
            "numero_enmascarado": tarjeta.numero_enmascarado,
            "exp_mes": tarjeta.exp_mes,
            "exp_ano": tarjeta.exp_ano,
            "default": tarjeta.default
        })
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def set_default_tarjeta(request, tarjeta_id):
    try:
        tarjeta = Tarjeta.objects.get(id=tarjeta_id, usuario=request.user)

        # Desmarcar otras tarjetas por defecto
        Tarjeta.objects.filter(usuario=request.user, default=True).update(default=False)
        tarjeta.default = True
        tarjeta.save()

        # Sincronizar con Stripe
        stripe.Customer.modify(
            request.user.stripe_customer_id,
            invoice_settings={"default_payment_method": tarjeta.token}
        )

        return Response({"detail": "Tarjeta marcada como por defecto"}, status=status.HTTP_200_OK)
    except Tarjeta.DoesNotExist:
        return Response({"error": "Tarjeta no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def eliminar_tarjeta(request, tarjeta_id):
    try:
        tarjeta = Tarjeta.objects.get(id=tarjeta_id, usuario=request.user)

        # Eliminar también en Stripe
        if tarjeta.token:
            try:
                stripe.PaymentMethod.detach(tarjeta.token)
            except stripe.error.StripeError as e:
                return Response({"error": f"No se pudo eliminar la tarjeta en Stripe: {str(e)}"},
                                status=status.HTTP_400_BAD_REQUEST)

        tarjeta.delete()
        return Response({"detail": "Tarjeta eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)
    except Tarjeta.DoesNotExist:
        return Response({"error": "Tarjeta no encontrada"}, status=status.HTTP_404_NOT_FOUND)
