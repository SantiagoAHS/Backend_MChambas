from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Service(models.Model):
    title = models.CharField(max_length=100)
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    reviews = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255)
    response_time = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'user')  # Un usuario solo puede dejar una reseña por servicio

    def __str__(self):
        return f'Review de {self.user} para {self.service.title}'


# Señales para actualizar automáticamente rating y reviews
@receiver([post_save, post_delete], sender=Review)
def update_service_rating_and_reviews(sender, instance, **kwargs):
    service = instance.service
    aggregate_data = service.service_reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    service.rating = round(aggregate_data['avg_rating'] or 0, 1)
    service.reviews = aggregate_data['total_reviews']
    service.save()
