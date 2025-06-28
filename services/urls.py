# services/urls.py
from django.urls import path
from .views import ServiceListCreateAPIView, create_service, services_by_user, update_service
from . import views

urlpatterns = [
    path('', ServiceListCreateAPIView.as_view(), name='services-list-create'),
    path('<int:pk>/', views.service_detail, name='service-detail'), 
    path('my-services/', services_by_user, name='services-by-user'),
    path('create/', create_service, name='create-service'),
    path('update/<int:pk>/', update_service, name='update_service'),

]
    
