from django.contrib import admin
from .models import Service, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'location', 'price', 'verified', 'rating', 'reviews')
    list_filter = ('verified', 'location', 'provider')
    search_fields = ('title', 'provider__email', 'location', 'description')
    ordering = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__email', 'service__title', 'comment')
    ordering = ('-created_at',)
