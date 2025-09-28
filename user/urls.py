from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ProfileUpdateView, VerifyUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    #Solo accesible por administradores
    path('verify/<int:user_id>/', VerifyUserView.as_view(), name='verify_user'),
]
