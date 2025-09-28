from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'nombre', 'password', 'telefono', 'avatar',
            'curp', 'identificacion', 'selfie_verificacion', 'is_verified'
        ]
        read_only_fields = ['is_verified']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Manejar archivos correctamente
        for file_field in ['avatar', 'identificacion', 'selfie_verificacion']:
            uploaded_file = validated_data.get(file_field)
            if uploaded_file is not None:
                setattr(instance, file_field, uploaded_file)
                validated_data.pop(file_field)

        # Actualizar los demás campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Cambiar la contraseña si se proporciona
        if password:
            instance.set_password(password)

        instance.save()
        return instance
