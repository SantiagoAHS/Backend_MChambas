from rest_framework import generics, permissions
from .models import Venta
from .serializers import VentaSerializer

# ===================
# EXISTENTE
# ===================
class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(comprador=self.request.user)


class VentaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]


# ===================
# NUEVAS VISTAS
# ===================

# 1️ Pedidos del comprador (lista)
class MisPedidosListAPIView(generics.ListAPIView):
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Venta.objects.filter(comprador=self.request.user)


# 2️ Detalle de un pedido del comprador
class MiPedidoDetailAPIView(generics.RetrieveAPIView):
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Venta.objects.filter(comprador=self.request.user)


# 3️ Ventas del vendedor (lista)
class MisVentasListAPIView(generics.ListAPIView):
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtramos las ventas de servicios creados por este proveedor
        return Venta.objects.filter(servicio__provider=self.request.user)


# 4️ Detalle de una venta del vendedor
class MiVentaDetailAPIView(generics.RetrieveAPIView):
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Venta.objects.filter(servicio__provider=self.request.user)
