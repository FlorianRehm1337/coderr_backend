from django.contrib import admin
from .models import CustomerProfile, BusinessProfile
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')
admin.site.register(CustomerProfile, UserAdmin)
admin.site.register(BusinessProfile, UserAdmin)
