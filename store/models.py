from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг (код)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название бренда")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    PROTOCOL_CHOICES = [
        ('Zigbee 3.0', 'Zigbee 3.0'),
        ('Matter', 'Matter'),
        ('Wi-Fi', 'Wi-Fi'),
        ('Bluetooth', 'Bluetooth'),
        ('Thread', 'Thread'),
    ]

    name = models.CharField(max_length=255, verbose_name="Наименование")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория"
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="products", verbose_name="Бренд"
    )
    generation = models.CharField(max_length=50, default="Gen 2", verbose_name="Поколение")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (₽)")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8, verbose_name="Рейтинг")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    description = models.TextField(verbose_name="Описание")

    # Технические характеристики
    protocol = models.CharField(
        max_length=50, choices=PROTOCOL_CHOICES, default='Zigbee 3.0', verbose_name="Протокол связи"
    )
    power = models.CharField(max_length=100, default="220V", verbose_name="Питание")
    dimensions = models.CharField(
        max_length=100, default="Стандартный типоразмер", verbose_name="Монтажные габариты"
    )
    ecosystem = models.JSONField(
        default=list, blank=True, verbose_name="Поддерживаемые экосистемы (список)"
    )
    manual = models.JSONField(
        default=list, blank=True, verbose_name="Инструкция по установке (пошагово)"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.price} ₽)"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Товар"
    )
    image_url = models.URLField(max_length=500, verbose_name="URL изображения")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ['order']

    def __str__(self):
        return f"Фото #{self.order} для {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер заказа")
    customer_name = models.CharField(max_length=150, verbose_name="Имя клиента")
    customer_email = models.EmailField(verbose_name="Email")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма (₽)")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус"
    )
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    items_data = models.JSONField(default=list, verbose_name="Позиции заказа (JSON)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ {self.order_number} ({self.total_price} ₽)"


class CustomRequest(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Товар"
    )
    product_name = models.CharField(max_length=255, verbose_name="Название товара")
    customer_name = models.CharField(max_length=150, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=50, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подачи заявки")

    class Meta:
        verbose_name = "Заявка «Под заказ»"
        verbose_name_plural = "Заявки «Под заказ»"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.customer_name} на {self.product_name}"