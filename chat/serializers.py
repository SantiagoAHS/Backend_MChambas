from rest_framework import serializers
from .models import Chat, Message
from user.serializers import UserSerializer  # Asumiendo tienes uno

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp']
        extra_kwargs = {
            'chat': {'required': False},
            'sender': {'required': False},
        }

class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at']
