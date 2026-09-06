from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from .models import Product
from .serializers import ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)  # Solo categorías activas
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Filtra productos por categoría si se pasa el parámetro 'category' en la URL."""
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset