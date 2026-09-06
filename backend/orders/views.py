from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Order
from .serializers import OrderCreateSerializer, OrderDetailSerializer

class OrderCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        s = OrderCreateSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        order = s.save()
        out = OrderDetailSerializer(order).data
        return Response(out, status=status.HTTP_201_CREATED)

class OrderDetailAPIView(APIView):
    permission_classes = [AllowAny]  # MVP invitado; en FASE 10 pediremos dueño

    def get(self, request, pk):
        order = Order.objects.filter(pk=pk).prefetch_related('items').first()
        if not order:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderDetailSerializer(order).data)