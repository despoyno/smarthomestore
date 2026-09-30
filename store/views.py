from rest_framework import viewsets, permissions
from .models import Category, Brand, Product, Order, CustomRequest
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    OrderSerializer,
    CustomRequestSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().prefetch_related('images', 'category', 'brand')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    """
    API для заказов. Возвращает заказы конкретного пользователя или все (если email не указан).
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(customer_email__iexact=email)
        return queryset


class CustomRequestViewSet(viewsets.ModelViewSet):
    queryset = CustomRequest.objects.all()
    serializer_class = CustomRequestSerializer
    permission_classes = [permissions.AllowAny]