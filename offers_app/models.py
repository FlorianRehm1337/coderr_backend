import json
from django.db import models
from django.contrib.auth.models import User
class Offer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='offer')
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=255)


class PackageDetail(models.Model):
    OFFER_TYPES = (
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    )

    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.PositiveIntegerField()
    delivery_time_in_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    features = models.ManyToManyField(Feature, related_name='package_details')

    def __str__(self):
        return f"{self.offer.title} - {self.title}"
