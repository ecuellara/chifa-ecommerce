from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'unit_price', 'subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo_entrega', 'metodo_pago', 'total', 'estado', 'created_at')
    list_filter = ('tipo_entrega', 'estado', 'metodo_pago')
    inlines = [OrderItemInline]