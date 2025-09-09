from django.db import models
from auth_app.models import CustomerProfile, BusinessProfile
from offers_app.models import Offer, PackageDetail

# Create your models here.
class Order(models.Model):
    customer_user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    business_user = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='orders')
    offer_detail = models.ForeignKey(PackageDetail, on_delete=models.CASCADE, related_name='orders', null=True)
    status = models.CharField(max_length=20, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
