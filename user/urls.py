from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ProfileUpdateView, UserVerifyViewSet, VerifyUserView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
     # 👇 NUEVAS RUTAS
    path('verify/users/', UserVerifyViewSet.as_view({'get': 'list'}), name='verify_users_list'),
    path('verify/users/<int:pk>/', UserVerifyViewSet.as_view({'patch': 'partial_update'}), name='verify_user_update'),

    #Solo accesible por administradores
    path('verify/<int:user_id>/', VerifyUserView.as_view(), name='verify_user'),
]
