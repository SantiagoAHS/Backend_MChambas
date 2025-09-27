from rest_framework import viewsets, permissions
from .models import Tarjeta
from .serializers import TarjetaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import stripe

class TarjetaViewSet(viewsets.ModelViewSet):
    serializer_class = TarjetaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tarjeta.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    # Acción para marcar tarjeta por defecto
    @action(detail=True, methods=['post'], url_path='set-default')  # <--- aquí
    def set_default(self, request, pk=None):
        try:
            tarjeta = self.get_object()
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
        
import stripe
from rest_framework import views, status
from rest_framework.response import Response
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class GuardarTarjetaStripeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        numero = request.data.get("numero")
        exp_mes = request.data.get("exp_mes")
        exp_ano = request.data.get("exp_ano")
        cvc = request.data.get("cvc")
        nombre_titular = request.data.get("nombre_titular")

        if not all([numero, exp_mes, exp_ano, cvc, nombre_titular]):
            return Response({"error": "Todos los campos son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": numero,
                    "exp_month": exp_mes,
                    "exp_year": exp_ano,
                    "cvc": cvc,
                },
            )

            tarjeta = Tarjeta.objects.create(
                usuario=request.user,
                nombre_titular=nombre_titular,
                numero_enmascarado=f"**** **** **** {payment_method.card.last4}",
                exp_mes=payment_method.card.exp_month,
                exp_ano=payment_method.card.exp_year,
                token=payment_method.id,
            )

            return Response({
                "id": tarjeta.id,
                "last4": payment_method.card.last4,
                "brand": payment_method.card.brand,
                "exp_mes": tarjeta.exp_mes,
                "exp_ano": tarjeta.exp_ano,
            }, status=status.HTTP_201_CREATED)

        except stripe.error.CardError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
