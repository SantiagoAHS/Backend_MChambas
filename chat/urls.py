from django.urls import path
from .views import user_chats, create_chat, send_message

urlpatterns = [
    path('', user_chats, name='user-chats'),
    path('create/', create_chat, name='create-chat'),
    path('<int:chat_id>/send/', send_message, name='send-message'),
]
