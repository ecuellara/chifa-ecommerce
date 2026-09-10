from django.db import models
from django.core.exceptions import ValidationError
from catalog.models import Product
from delivery.models import DeliveryZone
from django.contrib.auth.models import User

class Order(models.Model):
    DELIVERY = 'delivery'
    PICKUP = 'recojo'
    TYPE_CHOICES = [(DELIVERY, 'Delivery'), (PICKUP, 'Recojo en tienda')]

    PAYMENT_CHOICES = [
        ('yape', 'Yape/Plin'),
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
    ]
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparacion', 'En preparación'),
        ('camino', 'En camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    TRANSITIONS = {
        'pendiente': ['confirmado', 'cancelado'],
        'confirmado': ['preparacion', 'cancelado'],
        'preparacion': ['camino', 'cancelado'],
        'camino': ['entregado'],
        'entregado': [],
        'cancelado': [],
    }

    def can_transition(self, new_estado):
        return new_estado in self.TRANSITIONS.get(self.estado, [])

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    tipo_entrega = models.CharField(max_length=20, choices=TYPE_CHOICES, default=DELIVERY)
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20)
    zona = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    referencia = models.CharField(max_length=255, blank=True)
    metodo_pago = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='efectivo')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['estado', '-created_at'], name='order_estado_created_idx'),
            models.Index(fields=['telefono'], name='order_telefono_idx'),
            models.Index(fields=['user', '-created_at'], name='order_user_created_idx'),
        ]

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre} - S/. {self.total}"

    def clean(self):
        super().clean()
        if self.tipo_entrega == self.DELIVERY:
            if not self.zona:
                raise ValidationError({'zona': 'Delivery exige zona.'})
            if not (self.direccion or '').strip():
                raise ValidationError({'direccion': 'Delivery exige dirección.'})
        # validar transición solo si ya existe en DB (update, no create)
        if self.pk:
            try:
                old = Order.objects.get(pk=self.pk)
            except Order.DoesNotExist:
                return
            if old.estado != self.estado and not old.can_transition(self.estado):
                raise ValidationError({'estado': f"No puedes pasar de {old.estado} a {self.estado}."})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.qty} x {self.product_name}"