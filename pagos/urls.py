from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TarjetaViewSet
from .stripe_views import create_setup_intent, attach_payment_method

router = DefaultRouter()
router.register(r'tarjetas', TarjetaViewSet, basename='tarjetas')

urlpatterns = [
    path('', include(router.urls)),
    path('stripe/setup-intent/', create_setup_intent, name='stripe-setup-intent'),
    path('stripe/attach-payment-method/', attach_payment_method, name='stripe-attach-payment-method'),
]
