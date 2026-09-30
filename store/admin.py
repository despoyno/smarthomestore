from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage, Order, CustomRequest


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image_url', 'order')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'in_stock', 'rating', 'protocol')
    list_filter = ('category', 'brand', 'in_stock', 'protocol', 'generation')
    search_fields = ('name', 'description')
    list_editable = ('price', 'in_stock')
    inlines = [ProductImageInline]
    save_on_top = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_email', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'formatted_items_table')
    fields = (
        'order_number',
        'customer_name',
        'customer_email',
        'total_price',
        'status',
        'delivery_address',
        'formatted_items_table',
        'created_at'
    )
    save_on_top = True

    def formatted_items_table(self, obj):
        """Отображает красивую таблицу вместо сырого JSON"""
        if not obj.items_data or not isinstance(obj.items_data, list):
            return "Нет позиций"

        rows = []
        for item in obj.items_data:
            name = item.get('name', '—')
            qty = item.get('quantity', 1)
            price = float(item.get('price', 0))
            subtotal = qty * price
            rows.append(
                f"<tr style='border-bottom: 1px solid #374151;'>"
                f"<td style='padding: 8px 12px; font-weight: 500;'>{name}</td>"
                f"<td style='padding: 8px 12px; text-align: center; color: #9ca3af;'>{qty} шт.</td>"
                f"<td style='padding: 8px 12px; text-align: right;'>{price:,.2f} ₽</td>"
                f"<td style='padding: 8px 12px; text-align: right; font-weight: bold; color: #60a5fa;'>{subtotal:,.2f} ₽</td>"
                f"</tr>"
            )

        html = f"""
        <table style='width: 100%; max-width: 800px; border-collapse: collapse; background: #111827; color: #f3f4f6; border-radius: 8px; overflow: hidden; font-size: 13px;'>
            <thead>
                <tr style='background: #1f2937; text-align: left; font-size: 11px; text-transform: uppercase; color: #9ca3af;'>
                    <th style='padding: 10px 12px;'>Наименование позиции</th>
                    <th style='padding: 10px 12px; text-align: center;'>Кол-во</th>
                    <th style='padding: 10px 12px; text-align: right;'>Цена</th>
                    <th style='padding: 10px 12px; text-align: right;'>Сумма</th>
                </tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
        """
        return format_html(html)

    formatted_items_table.short_description = "Состав заказа (товарная накладная)"


@admin.register(CustomRequest)
class CustomRequestAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'customer_name', 'customer_phone', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'product_name')
    readonly_fields = ('created_at',)
    save_on_top = True