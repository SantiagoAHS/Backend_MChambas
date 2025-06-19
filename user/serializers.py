from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'nombre', 'password', 'telefono', 'avatar']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Si se quiere cambiar la contraseña
        password = validated_data.pop('password', None)

        # Actualiza los demás campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Cambiar la contraseña de forma segura
        if password:
            instance.set_password(password)

        instance.save()
        return instance
