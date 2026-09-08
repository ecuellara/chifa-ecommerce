from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class StaffCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all().order_by('order', 'name')
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name', '')
        serializer.save(slug=slugify(name))


class StaffProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all().select_related('category').order_by('order', 'name')
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name', '')
        serializer.save(slug=slugify(name))
