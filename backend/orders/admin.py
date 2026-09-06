from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'unit_price', 'subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo_entrega', 'total', 'estado', 'created_at')
    list_filter = ('estado', 'tipo_entrega', 'metodo_pago')
    search_fields = ('nombre', 'telefono', 'id')
    readonly_fields = ('subtotal', 'delivery_cost', 'total', 'created_at')