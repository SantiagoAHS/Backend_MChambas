from django.db import models
from django.conf import settings

class Tarjeta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tarjetas')
    nombre_titular = models.CharField(max_length=100)
    numero_enmascarado = models.CharField(max_length=19)  # Ej: '**** **** **** 1234'
    exp_mes = models.PositiveSmallIntegerField()  # 1-12
    exp_ano = models.PositiveSmallIntegerField()  # Ej: 2025
    token = models.CharField(max_length=100, blank=True, null=True)  # para guardar token si usas proveedor externo
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    default = models.BooleanField(default=False)  # indica si es la tarjeta por defecto

    def __str__(self):
        return f"{self.nombre_titular} - {self.numero_enmascarado}"
