from rest_framework import serializers
from .models import Tarjeta

class TarjetaSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(write_only=True)  # campo extra para recibir el número completo

    class Meta:
        model = Tarjeta
        fields = ['id', 'nombre_titular', 'numero_enmascarado', 'exp_mes', 'exp_ano', 'numero']
        read_only_fields = ['id', 'numero_enmascarado']

    def create(self, validated_data):
        usuario = self.context['request'].user
        numero = validated_data.pop('numero')  # recibir número completo para enmascarar

        numero_enmascarado = '**** **** **** ' + numero[-4:]

        tarjeta = Tarjeta.objects.create(
            usuario=usuario,
            numero_enmascarado=numero_enmascarado,
            **validated_data
        )
        return tarjeta