from django.contrib import admin
from .models import DeliveryZone

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'is_active')
    list_filter = ('is_active',)