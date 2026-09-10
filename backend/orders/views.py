from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from .models import Order
from .serializers import OrderCreateSerializer, OrderDetailSerializer


class OrderBurstThrottle(AnonRateThrottle):
    scope = 'order_burst'


class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OrderBurstThrottle]

    def post(self, request):
        s = OrderCreateSerializer(data=request.data, context={'request': request})
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        order = s.save()
        out = OrderDetailSerializer(order).data
        return Response(out, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        order = Order.objects.filter(pk=pk).prefetch_related('items').first()
        if not order:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        if order.user:
            if not request.user.is_authenticated or order.user_id != request.user.id:
                return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(OrderDetailSerializer(order).data)
        # invitado: exige ?telefono= igual que track
        tel = request.query_params.get('telefono', '').strip()
        if not tel or order.telefono != tel:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderDetailSerializer(order).data)


class OrderTrackAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order_id = request.query_params.get('id', '').strip()
        telefono = request.query_params.get('telefono', '').strip()
        if not order_id or not telefono:
            return Response({'detail': 'Indica id y telefono.'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(id=order_id, telefono=telefono).prefetch_related('items').first()
        if not order:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderDetailSerializer(order).data)


class MyOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Order.objects.filter(user=request.user).prefetch_related('items')
        return Response(OrderDetailSerializer(qs, many=True).data)
