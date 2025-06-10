from django.contrib import admin
from .models import Offer, Feature, PackageDetail
from offers_app.models import Feature, Offer, PackageDetail

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class PackageDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(Offer, OfferAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(PackageDetail, PackageDetailAdmin)
