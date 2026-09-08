from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import DeliveryZone
from .serializers import DeliveryZoneSerializer


class StaffDeliveryZoneViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = DeliveryZone.objects.all().order_by('sort_order', 'cost')
    serializer_class = DeliveryZoneSerializer
