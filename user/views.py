from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

# ========================
# Registro
# ========================
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


# ========================
# Login
# ========================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response({"error": "Credenciales inválidas"}, status=400)


# ========================
# Perfil del usuario
# ========================
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "nombre": getattr(user, "nombre", ""),
            "telefono": getattr(user, "telefono", ""),
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None,
            "curp": getattr(user, "curp", ""),
            "identificacion": request.build_absolute_uri(user.identificacion.url) if user.identificacion else None,
            "selfie_verificacion": request.build_absolute_uri(user.selfie_verificacion.url) if user.selfie_verificacion else None,
            "is_verified": user.is_verified,
        })

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ========================
# Actualización de perfil con archivos
# ========================
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Para manejar imágenes/PDF

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================
# Verificación de usuarios (solo admin)
# ========================
class VerifyUserView(APIView):
    permission_classes = [IsAdminUser]  # Solo admin puede verificar

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()
            return Response({"message": f"El usuario {user.email} ha sido verificado."})
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
