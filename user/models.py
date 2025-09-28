from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # NUEVO → Verificación de identidad
    curp = models.CharField(max_length=18, blank=True, null=True, unique=True)
    identificacion = models.FileField(upload_to="identificaciones/", blank=True, null=True)
    selfie_verificacion = models.ImageField(upload_to="selfies_verificacion/", blank=True, null=True)

    # Estado de verificación
    is_verified = models.BooleanField(default=False)

    # Stripe
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    # Campos estándar de Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email
