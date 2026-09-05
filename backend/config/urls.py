from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet

# Creamos un router y registramos nuestro ViewSet
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Todas las rutas del router estarán bajo /api/
]