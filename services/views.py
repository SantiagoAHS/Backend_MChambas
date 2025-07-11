from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

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
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(provider=request.user)
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




