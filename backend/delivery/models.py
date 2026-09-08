from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class DeliveryZone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_time = models.CharField(max_length=50, blank=True)
    min_order = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    free_over = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'cost', 'name']
        verbose_name = "Zona de delivery"
        verbose_name_plural = "Zonas de delivery"

    def __str__(self):
        return f"{self.name} - S/. {self.cost}"

    def clean(self):
        super().clean()
        if self.cost is not None and self.cost < 0:
            raise ValidationError({'cost': 'El costo no puede ser negativo.'})
        if self.free_over is not None and self.free_over <= self.cost:
            raise ValidationError({'free_over': 'Gratis debe ser mayor al costo.'})

    def get_delivery_cost(self, subtotal):
        if self.free_over is not None and subtotal >= self.free_over:
            return Decimal('0')
        return self.cost