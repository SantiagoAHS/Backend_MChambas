from rest_framework import serializers
from .models import Tarjeta

class TarjetaSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(write_only=True, required=False)  # opcional, solo para crear

    class Meta:
        model = Tarjeta
        fields = ['id', 'nombre_titular', 'numero_enmascarado', 'exp_mes', 'exp_ano', 'default', 'numero']
        read_only_fields = ['id', 'numero_enmascarado', 'default']

    def create(self, validated_data):
        usuario = self.context['request'].user
        numero = validated_data.pop('numero', None)  # recibir número completo si viene

        numero_enmascarado = '**** **** **** ' + (numero[-4:] if numero else '0000')

        tarjeta = Tarjeta.objects.create(
            usuario=usuario,
            numero_enmascarado=numero_enmascarado,
            **validated_data
        )
        return tarjeta
