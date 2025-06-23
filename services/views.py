from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Service
from .serializers import ServiceSerializer

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
@permission_classes([AllowAny])  # <-- Aquí permites acceso público
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
