from rest_framework import generics, permissions
from .models import Venta
from .serializers import VentaSerializer
from rest_framework.response import Response

# ===================
# EXISTENTE
# ===================
class VentaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Aquí asignas el comprador desde el usuario autenticado
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


# 4️ Detalle y actualización de estado de una venta del vendedor
class MiVentaDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Venta.objects.filter(servicio__provider=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = True  # Permite actualizar campos parciales
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


