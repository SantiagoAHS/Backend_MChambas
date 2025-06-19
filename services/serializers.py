# services/serializers.py
from rest_framework import serializers
from .models import Service
from user.serializers import UserSerializer

class ServiceSerializer(serializers.ModelSerializer):
    provider = UserSerializer(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'provider', 'image', 'verified', 'description',
            'rating', 'reviews', 'location', 'response_time', 'price', 'created_at'
        ]
