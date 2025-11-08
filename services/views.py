from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils import validar_direccion_nominatim
from .models import Service, Review
from .serializers import ServiceSerializer
from .serializers import ReviewSerializer


class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('-created_at')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

class ServiceListAPIView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]  # 🔹 cualquiera puede ver los servicios

    def get_queryset(self):
        queryset = Service.objects.all()
        location = self.request.query_params.get("location")
        verified = self.request.query_params.get("verified")
        price_range = self.request.query_params.get("price")  # ahora recibe el rango completo
        min_rating = self.request.query_params.get("rating")

        if location:
            queryset = queryset.filter(location__icontains=location)
        if verified == "true":
            queryset = queryset.filter(verified=True)
        if price_range:
            try:
                if "-" in price_range:  # rango
                    min_price, max_price = map(int, price_range.split("-"))
                    queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
                elif price_range.startswith("<"):  # menor que
                    max_price = int(price_range[1:])
                    queryset = queryset.filter(price__lte=max_price)
                elif price_range.startswith(">"):  # mayor que
                    min_price = int(price_range[1:])
                    queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=int(min_rating))
            except ValueError:
                pass

        return queryset

@api_view(['GET'])
@permission_classes([AllowAny])  
def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return Response({'error': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceSerializer(service)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def services_by_user(request):
    user = request.user
    services = Service.objects.filter(provider=user)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service(request):
    user = request.user

    # Bloquear si el usuario no está verificado
    if not user.is_verified:
        return Response(
            {"error": "Tu cuenta no está verificada. No puedes crear servicios."},
            status=status.HTTP_403_FORBIDDEN
        )

    # 👇 Clonamos request.data en un diccionario mutable
    data = request.data.copy()

    street = data.get("street")
    city = data.get("city")
    state = data.get("state")
    country = data.get("country")
    postalcode = data.get("postalcode")

    direccion_validada = validar_direccion_nominatim(
        street=street,
        city=city,
        state=state,
        country=country,
        postalcode=postalcode
    )

    if not direccion_validada:
        return Response({"error": "No se pudo validar la dirección"}, status=status.HTTP_400_BAD_REQUEST)

    # 👇 Ahora sí puedes modificar el diccionario
    data["location"] = direccion_validada.get("display_name", "")

    serializer = ServiceSerializer(data=data)
    if serializer.is_valid():
        serializer.save(provider=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_service(request, pk):
    try:
        service = Service.objects.get(pk=pk, provider=request.user)
    except Service.DoesNotExist:
        return Response({'error': 'Servicio no encontrado o no autorizado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceSerializer(service, data=request.data, partial=True)  # `partial=True` permite actualizar campos individuales
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return Response({'error': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Evitar que un usuario comente dos veces el mismo servicio
    if Review.objects.filter(service=service, user=request.user).exists():
        return Response({'error': 'Ya enviaste una reseña para este servicio'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(service=service, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_reviews(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return Response({'error': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    reviews = Review.objects.filter(service=service).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ServiceVerifyViewSet(viewsets.ViewSet):
    """
    Vista para listar servicios y actualizar su verificación manualmente.
    No usa permisos especiales, pero se recomienda ocultarla en el frontend.
    """
    permission_classes = [permissions.AllowAny]

    # 🔹 Listar todos los servicios
    def list(self, request):
        services = Service.objects.all().order_by('-id')
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    # 🔹 Actualizar el estado de verificación
    def partial_update(self, request, pk=None):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({"error": "Servicio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        verified = request.data.get("verified")
        if verified is not None:
            service.verified = verified
            service.save()
            return Response({"message": "Estado de verificación actualizado correctamente."})

        return Response({"error": "Campo no permitido"}, status=status.HTTP_400_BAD_REQUEST)



