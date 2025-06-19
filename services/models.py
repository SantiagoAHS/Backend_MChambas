# services/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Service(models.Model):
    title = models.CharField(max_length=100)
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    reviews = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100)
    response_time = models.CharField(max_length=50)
    price = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
