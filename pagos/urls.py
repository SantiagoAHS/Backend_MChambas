from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TarjetaViewSet

router = DefaultRouter()
router.register(r'tarjetas', TarjetaViewSet, basename='tarjetas')

urlpatterns = [
    path('', include(router.urls)),
]