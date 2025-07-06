from django.db import models
from django.conf import settings

class Chat(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats',
        verbose_name='Participantes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nombres = ", ".join([user.nombre for user in self.participants.all()])
        return f"Chat entre {nombres}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender.nombre} en Chat {self.chat.id}"
