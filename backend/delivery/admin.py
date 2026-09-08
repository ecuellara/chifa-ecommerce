from django.contrib import admin
from .models import DeliveryZone

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'free_over', 'min_order', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('cost', 'free_over', 'min_order', 'sort_order', 'is_active')