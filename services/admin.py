from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'location', 'price', 'verified', 'rating')
    list_filter = ('verified', 'location', 'provider')
    search_fields = ('title', 'provider__email', 'location', 'description')
    ordering = ('title',)

    # Si quieres mostrar la imagen en miniatura en el admin (opcional)
    # def avatar_preview(self, obj):
    #     if obj.avatar:
    #         return format_html('<img src="{}" width="50" height="50" />'.format(obj.avatar.url))
    #     return "-"
    # avatar_preview.short_description = 'Avatar'

