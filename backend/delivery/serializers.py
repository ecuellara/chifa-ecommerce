from rest_framework import serializers
from .models import DeliveryZone

class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = ['id', 'name', 'cost', 'estimated_time']