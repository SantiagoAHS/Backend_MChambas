from rest_framework import viewsets, permissions
from .models import Tarjeta
from .serializers import TarjetaSerializer

class TarjetaViewSet(viewsets.ModelViewSet):
    serializer_class = TarjetaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # solo tarjetas del usuario autenticado
        return Tarjeta.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # El usuario ya se asigna dentro del serializer, no pasar usuario aquí
        serializer.save()
