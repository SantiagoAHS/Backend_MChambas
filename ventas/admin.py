from django.contrib import admin
from .models import Venta

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprador', 'servicio', 'fecha', 'estado', 'cantidad', 'total')
    list_filter = ('estado', 'fecha')
    search_fields = ('comprador__username', 'servicio__title', 'address', 'city')

    readonly_fields = ('total', 'fecha')  # total y fecha no editables en el formulario admin
