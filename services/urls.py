# services/urls.py
from django.urls import path
from .views import ServiceListCreateAPIView
from django.urls import include

urlpatterns = [
    path('', ServiceListCreateAPIView.as_view(), name='services-list-create'),
]
