from django.urls import path
from .views import (
    ServiceListCreateAPIView,
    ServiceListAPIView, 
    create_review,
    create_service,
    list_reviews,
    services_by_user,
    update_service,
    service_detail,
    ServiceVerifyViewSet,  # 👈 Importamos la nueva vista
)

# 👇 Añadimos las vistas de verificación manual
service_verify_list = ServiceVerifyViewSet.as_view({
    'get': 'list',
})

service_verify_update = ServiceVerifyViewSet.as_view({
    'patch': 'partial_update',
})

urlpatterns = [
    path('', ServiceListCreateAPIView.as_view(), name='services-list-create'),
    path('filtered/', ServiceListAPIView.as_view(), name='services-list-filtered'),
    path('<int:pk>/', service_detail, name='service-detail'), 
    path('my-services/', services_by_user, name='services-by-user'),
    path('create/', create_service, name='create-service'),
    path('update/<int:pk>/', update_service, name='update_service'),
    path('<int:service_id>/reviews/', list_reviews, name='list-reviews'),
    path('<int:service_id>/reviews/create/', create_review, name='create-review'),

    # 🔹 Nuevas rutas para verificación de servicios
    path('verify/services/', service_verify_list, name='service-verify-list'),
    path('verify/services/<int:pk>/', service_verify_update, name='service-verify-update'),
]
