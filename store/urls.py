from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    CategoryViewSet,
    BrandViewSet,
    OrderViewSet,
    CustomRequestViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'requests', CustomRequestViewSet, basename='request')

urlpatterns = [
    path('', include(router.urls)),
]