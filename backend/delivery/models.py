from django.db import models

class DeliveryZone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_time = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['cost', 'name']
        verbose_name = "Zona de delivery"
        verbose_name_plural = "Zonas de delivery"

    def __str__(self):
        return f"{self.name} - S/. {self.cost}"