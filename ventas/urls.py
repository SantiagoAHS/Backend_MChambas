from django.urls import path
from . import views

urlpatterns = [
    path('', views.VentaListCreateAPIView.as_view(), name='ventas-list-create'),  # GET lista / POST crea
    path('<int:pk>/', views.VentaDetailAPIView.as_view(), name='venta-detail'),  # GET, PUT, PATCH, DELETE por ID
    # Comprador
    path('mis-pedidos/', views.MisPedidosListAPIView.as_view(), name='mis-pedidos'),
    path('mis-pedidos/<int:pk>/', views.MiPedidoDetailAPIView.as_view(), name='mi-pedido-detail'),

    # Vendedor
    path('mis-ventas/', views.MisVentasListAPIView.as_view(), name='mis-ventas'),
    path('mis-ventas/<int:pk>/', views.MiVentaDetailAPIView.as_view(), name='mi-venta-detail'),
]
