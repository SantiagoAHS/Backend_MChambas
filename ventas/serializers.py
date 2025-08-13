from rest_framework import serializers
from .models import Venta
from services.models import Service

class ServiceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'price']

class VentaSerializer(serializers.ModelSerializer):
    comprador = serializers.ReadOnlyField(source='comprador.nombre')
    servicio = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        write_only=True
    )
    servicio_detalle = ServiceMiniSerializer(source='servicio', read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id',
            'comprador',
            'servicio',         # para input (POST)
            'servicio_detalle', # para output (GET)
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
        read_only_fields = ['total', 'fecha','comprador']

    def validate_estado(self, value):
        estados_validos = ['pendiente', 'iniciado', 'procesando', 'cancelado', 'completado']
        if value not in estados_validos:
            raise serializers.ValidationError("Estado no válido.")
        return value

    def create(self, validated_data):
        # 'servicio' está en validated_data como instancia Service porque es PrimaryKeyRelatedField
        return Venta.objects.create(**validated_data)
