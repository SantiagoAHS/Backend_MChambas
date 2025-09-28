from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'id', 
        'email', 
        'nombre', 
        'show_avatar', 
        'curp', 
        'identificacion', 
        'is_verified', 
        'is_staff', 
        'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'nombre', 'curp')
    ordering = ('id',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'nombre', 'telefono', 'avatar')
        }),
        ('Verificación', {
            'fields': ('curp', 'identificacion', 'is_verified')
        }),
        ('Permisos', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'nombre', 'telefono', 'avatar',
                'curp', 'identificacion', 'is_verified',
                'is_staff', 'is_active'
            ),
        }),
    )

    def show_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.avatar.url)
        return "Sin avatar"
    show_avatar.short_description = "Avatar"
