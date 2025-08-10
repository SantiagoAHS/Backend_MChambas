from django.db import models
from django.conf import settings
from services.models import Service

class Venta(models.Model):
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compras'
    )
    servicio = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('pagado', 'Pagado'),
            ('cancelado', 'Cancelado'),
            ('completado', 'Completado'),
        ],
        default='pendiente'
    )
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Campos del formulario
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.comprador.nombre} compró {self.servicio.title}'

    def save(self, *args, **kwargs):
        self.total = self.servicio.price * self.cantidad
        super().save(*args, **kwargs)
