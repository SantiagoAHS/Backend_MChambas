from rest_framework import serializers
from .models import Venta
from services.models import Service

class ServiceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'price'] 

class VentaSerializer(serializers.ModelSerializer):
    comprador = serializers.ReadOnlyField(source='comprador.nombre')  
    servicio = ServiceMiniSerializer(read_only=True)  # Aquí el serializer anidado

    class Meta:
        model = Venta
        fields = [
            'id',
            'comprador',
            'servicio',   # ahora este incluirá title y price
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
        read_only_fields = ['total', 'fecha', 'estado']

