# ✅ services/urls.py
from django.urls import path
from .views import ServiceListCreateAPIView, services_by_user
from . import views

urlpatterns = [
    path('', ServiceListCreateAPIView.as_view(), name='services-list-create'),
    path('<int:pk>/', views.service_detail, name='service-detail'), 
    path('my-services/', services_by_user, name='services-by-user'),
]
