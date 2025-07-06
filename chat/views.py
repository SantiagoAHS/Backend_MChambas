from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_chats(request):
    user = request.user
    chats = Chat.objects.filter(participants=user).order_by('-created_at')
    serializer = ChatSerializer(chats, many=True)
    return Response({
        "user_id": user.id,  # Aquí enviamos el userId para frontend
        "chats": serializer.data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat(request):
    user = request.user
    other_user_id = request.data.get("other_user_id")

    if not other_user_id:
        return Response({'error': 'Se requiere other_user_id'}, status=status.HTTP_400_BAD_REQUEST)

    if int(other_user_id) == user.id:
        return Response({'error': 'No puedes crear un chat contigo mismo'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si ya existe un chat con esos dos participantes (sin importar orden)
    chats = Chat.objects.filter(participants=user).filter(participants__id=other_user_id).distinct()
    if chats.exists():
        chat = chats.first()
    else:
        chat = Chat.objects.create()
        chat.participants.add(user.id, other_user_id)
        chat.save()

    serializer = ChatSerializer(chat)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    user = request.user
    try:
        chat = Chat.objects.get(id=chat_id, participants=user)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat no encontrado o acceso denegado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=user, chat=chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
