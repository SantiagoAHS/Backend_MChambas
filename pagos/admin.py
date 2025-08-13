from django.contrib import admin
from .models import Tarjeta

@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'numero_enmascarado', 'nombre_titular')  # ajusta campos que tengas
    search_fields = ('usuario__username', 'nombre_titular', 'numero')

    def numero_enmascarado(self, obj):
        return '**** **** **** ' + obj.numero[-4:]
    numero_enmascarado.short_description = 'Número de Tarjeta'