from rest_framework import serializers
from .models import Category
from .models import Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'order']
        read_only_fields = ['id', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'category_slug',
            'name', 'slug', 'description', 'price',
            'image', 'is_active', 'is_featured', 'order'
        ]
        read_only_fields = ['id', 'slug']