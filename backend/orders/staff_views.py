from django.db.models import Count, Sum, Avg
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import Order
from .serializers import OrderDetailSerializer

class StaffOrderListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        qs = Order.objects.all().select_related('zona', 'user').prefetch_related('items')
        estado = request.query_params.get('estado', '').strip()
        if estado:
            qs = qs.filter(estado=estado)
        qs = qs.order_by('-created_at')[:100]
        return Response(OrderDetailSerializer(qs, many=True).data)

class StaffOrderPatchAPIView(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, pk):
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response({'detail': 'No encontrado.'}, status=404)
        nuevo = request.data.get('estado', '').strip()
        if nuevo not in dict(Order.STATUS_CHOICES):
            return Response({'estado': 'Estado inválido.'}, status=400)
        if not order.can_transition(nuevo):
            return Response({'estado': f'No puedes pasar de {order.estado} a {nuevo}.'}, status=400)
        order.estado = nuevo
        try:
            order.full_clean()
        except Exception as e:
            return Response({'estado': str(e)}, status=400)
        order.save(update_fields=['estado'])
        return Response(OrderDetailSerializer(order).data)

class StaffStatsAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        hoy = timezone.localdate()
        base = Order.objects.filter(created_at__date=hoy)
        agg = base.aggregate(n=Count('id'), ventas=Sum('total'), ticket=Avg('total'))
        por_estado = list(base.values('estado').annotate(n=Count('id')).order_by('estado'))
        return Response({
            'fecha': str(hoy),
            'n_hoy': agg['n'] or 0,
            'ventas_hoy': str(agg['ventas'] or 0),
            'ticket_hoy': str(round(agg['ticket'] or 0, 2)),
            'por_estado': por_estado,
        })