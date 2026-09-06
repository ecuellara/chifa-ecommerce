from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from catalog.models import Product
from delivery.models import DeliveryZone
from .models import Order, OrderItem

class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    tipo_entrega = serializers.ChoiceField(choices=['delivery', 'recojo'])
    nombre = serializers.CharField(max_length=120)
    telefono = serializers.CharField(max_length=20)
    zona_id = serializers.IntegerField(required=False, allow_null=True)
    direccion = serializers.CharField(required=False, allow_blank=True, default='')
    referencia = serializers.CharField(required=False, allow_blank=True, default='')
    metodo_pago = serializers.ChoiceField(choices=['yape', 'tarjeta', 'efectivo'])
    items = OrderItemInputSerializer(many=True)

    def validate(self, attrs):
        if not attrs.get('items'):
            raise serializers.ValidationError('El carrito está vacío.')
        if attrs['tipo_entrega'] == 'delivery' and not attrs.get('zona_id'):
            raise serializers.ValidationError({'zona_id': 'Delivery exige zona.'})
        if attrs['tipo_entrega'] == 'delivery' and not attrs.get('direccion', '').strip():
            raise serializers.ValidationError({'direccion': 'Delivery exige dirección.'})
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        zona_id = validated_data.pop('zona_id', None)

        with transaction.atomic():
            zona = None
            delivery_cost = Decimal('0')
            if validated_data['tipo_entrega'] == 'delivery':
                zona = DeliveryZone.objects.filter(id=zona_id, is_active=True).first()
                if not zona:
                    raise serializers.ValidationError({'zona_id': 'Zona inválida.'})
                delivery_cost = zona.cost

            order = Order.objects.create(
                zona=zona,
                direccion=validated_data.get('direccion', ''),
                delivery_cost=delivery_cost,
                **{k: v for k, v in validated_data.items() if k not in ('zona_id', 'direccion')},
            )

            subtotal = Decimal('0')
            for it in items_data:
                product = Product.objects.filter(id=it['product_id'], is_active=True).first()
                if not product:
                    raise serializers.ValidationError(f"Producto {it['product_id']} no disponible.")
                unit = product.price
                line = unit * it['qty']
                subtotal += line
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    unit_price=unit,
                    qty=it['qty'],
                    subtotal=line,
                )

            order.subtotal = subtotal
            order.total = subtotal + delivery_cost
            order.save(update_fields=['subtotal', 'total'])
            return order

class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    zona_name = serializers.CharField(source='zona.name', read_only=True, default=None)

    class Meta:
        model = Order
        fields = ['id', 'tipo_entrega', 'nombre', 'telefono', 'zona', 'zona_name',
                  'direccion', 'referencia', 'metodo_pago', 'subtotal',
                  'delivery_cost', 'total', 'estado', 'created_at', 'items']

    def get_items(self, obj):
        return [{'product_name': i.product_name, 'qty': i.qty,
                 'unit_price': str(i.unit_price), 'subtotal': str(i.subtotal)}
                for i in obj.items.all()]