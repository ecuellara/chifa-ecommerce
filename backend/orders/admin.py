from django.contrib import admin
from django.db.models import Count, Sum, Avg
from .models import Order, OrderItem


def _avanzar(modeladmin, request, queryset, destino):
    ok, bloqueados = 0, 0
    for order in queryset:
        if order.can_transition(destino):
            order.estado = destino
            try:
                order.full_clean()
                order.save(update_fields=['estado'])
                ok += 1
            except Exception:
                bloqueados += 1
        else:
            bloqueados += 1
    modeladmin.message_user(request, f"{ok} a {destino}, {bloqueados} bloqueados por transición inválida.")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'unit_price', 'subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'user', 'tipo_entrega', 'zona', 'total', 'estado', 'created_at')
    list_filter = ('estado', 'tipo_entrega', 'metodo_pago')
    search_fields = ('nombre', 'telefono', 'id', 'user__username')
    readonly_fields = ('subtotal', 'delivery_cost', 'total', 'created_at')
    date_hierarchy = 'created_at'
    list_select_related = ('zona', 'user')
    inlines = [OrderItemInline]
    actions = ('a_confirmado', 'a_preparacion', 'a_camino', 'a_entregado', 'a_cancelado')

    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request)
        stats = qs.aggregate(
            n=Count('id'),
            ventas=Sum('total'),
            ticket=Avg('total'),
        )
        extra_context = extra_context or {}
        extra_context['stats'] = {
            'n': stats['n'] or 0,
            'ventas': stats['ventas'] or 0,
            'ticket': round(stats['ticket'] or 0, 2),
        }
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description='Pasar a confirmado')
    def a_confirmado(self, request, qs):
        _avanzar(self, request, qs, 'confirmado')

    @admin.action(description='Pasar a preparación')
    def a_preparacion(self, request, qs):
        _avanzar(self, request, qs, 'preparacion')

    @admin.action(description='Pasar a en camino')
    def a_camino(self, request, qs):
        _avanzar(self, request, qs, 'camino')

    @admin.action(description='Pasar a entregado')
    def a_entregado(self, request, qs):
        _avanzar(self, request, qs, 'entregado')

    @admin.action(description='Cancelar')
    def a_cancelado(self, request, qs):
        _avanzar(self, request, qs, 'cancelado')