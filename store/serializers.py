from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, Order, CustomRequest


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    # Приводим id к строке, а цену и рейтинг — к числам с плавающей точкой
    id = serializers.CharField(read_only=True)
    price = serializers.FloatField()
    rating = serializers.FloatField()

    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    brand = serializers.SlugRelatedField(read_only=True, slug_field='name')
    inStock = serializers.BooleanField(source='in_stock', read_only=True)

    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    specs = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'brand',
            'category',
            'generation',
            'price',
            'rating',
            'image',
            'images',
            'description',
            'specs',
            'manual',
            'inStock'
        ]

    def get_image(self, obj):
        first_img = obj.images.first()
        return first_img.image_url if first_img else ""

    def get_images(self, obj):
        return [img.image_url for img in obj.images.all()]

    def get_specs(self, obj):
        return {
            'protocol': obj.protocol,
            'power': obj.power,
            'dimensions': obj.dimensions,
            'ecosystem': obj.ecosystem if isinstance(obj.ecosystem, list) else []
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'customer_email',
            'total_price',
            'status',
            'delivery_address',
            'items_data',
            'created_at'
        ]


class CustomRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRequest
        fields = [
            'id',
            'product',
            'product_name',
            'customer_name',
            'customer_phone',
            'comment',
            'created_at'
        ]