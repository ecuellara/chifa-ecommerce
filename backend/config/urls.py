from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet, ProductViewSet
from delivery.views import DeliveryZoneViewSet
from orders.views import MyOrdersListAPIView, OrderCreateAPIView, OrderDetailAPIView, OrderTrackAPIView
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import RegisterAPIView, CustomLoginView, MeAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from orders.staff_views import StaffOrderListAPIView, StaffOrderPatchAPIView, StaffStatsAPIView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'zones', DeliveryZoneViewSet, basename='zone')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/orders/', OrderCreateAPIView.as_view(), name='order-create'),
    path('api/orders/track/', OrderTrackAPIView.as_view(), name='order-track'),
    path('api/orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('api/auth/login/', CustomLoginView.as_view(), name='auth-login'),
    path('api/auth/me/', MeAPIView.as_view(), name='auth-me'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('api/my-orders/', MyOrdersListAPIView.as_view(), name='my-orders'),
    path('api/staff/orders/', StaffOrderListAPIView.as_view(), name='staff-orders'),
    path('api/staff/orders/<int:pk>/', StaffOrderPatchAPIView.as_view(), name='staff-order-patch'),
    path('api/staff/stats/', StaffStatsAPIView.as_view(), name='staff-stats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)