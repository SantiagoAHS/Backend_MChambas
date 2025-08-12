from rest_framework import serializers
from .models import Venta
from services.models import Service

class ServiceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'price'] 

class VentaSerializer(serializers.ModelSerializer):
    comprador = serializers.ReadOnlyField(source='comprador.nombre')  
    servicio = ServiceMiniSerializer(read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id',
            'comprador',
            'servicio',
            'cantidad',
            'total',
            'fecha',
            'estado',
            'address',
            'city',
            'state',
            'postal_code',
            'phone',
        ]
        read_only_fields = ['total', 'fecha']  # quitamos 'estado'

    def validate_estado(self, value):
        # Solo permitir estados válidos
        estados_validos = ['pendiente', 'iniciado', 'procesando', 'cancelado', 'completado']
        if value not in estados_validos:
            raise serializers.ValidationError("Estado no válido.")
        return value


