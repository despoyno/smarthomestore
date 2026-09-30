from django.core.management.base import BaseCommand
from store.models import Category, Brand, Product, ProductImage

class Command(BaseCommand):
    help = 'Заполняет базу данных 50 реальными товарами умного дома'

    def handle(self, *args, **options):
        # 1. Категории
        categories_map = {
            'lighting': 'Освещение',
            'sensors': 'Датчики',
            'hubs': 'Хабы и шлюзы',
            'security': 'Безопасность',
            'climate': 'Климат',
            'sockets': 'Розетки и реле',
        }
        cat_objs = {}
        for slug, name in categories_map.items():
            obj, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            cat_objs[slug] = obj

        # 2. Бренды
        brands = ['Philips Hue', 'Aqara', 'Tuya', 'Sonoff', 'Яндекс']
        brand_objs = {}
        for b in brands:
            obj, _ = Brand.objects.get_or_create(name=b)
            brand_objs[b] = obj

        # 3. Товары (выгрузка из нашего датасета)
        from store.initial_dataset import RAW_DEVICES

        created_count = 0
        for dev in RAW_DEVICES:
            brand_obj = brand_objs.get(dev['brand'])
            cat_obj = cat_objs.get(dev['category'])

            product, created = Product.objects.get_or_create(
                name=dev['name'],
                defaults={
                    'category': cat_obj,
                    'brand': brand_obj,
                    'generation': dev['generation'],
                    'price': dev['price'],
                    'protocol': dev['protocol'],
                    'in_stock': dev['inStock'],
                    'description': dev['desc'],
                    'power': dev['power'],
                    'ecosystem': ['Яндекс', 'Apple HomeKit', 'Home Assistant', 'Tuya'],
                    'manual': [
                        'Обесточьте линию питания или удалите изолирующую ленту.',
                        'Зажмите кнопку сопряжения на 5 секунд до мигания индикатора.',
                        'В приложении умного дома запустите поиск новых Zigbee/Matter устройств.',
                        'Задайте имя устройству и выберите комнату.'
                    ]
                }
            )

            if created:
                created_count += 1
                for idx, img_url in enumerate(dev['images']):
                    ProductImage.objects.create(
                        product=product,
                        image_url=img_url,
                        order=idx
                    )

        self.stdout.write(self.style.SUCCESS(f'Успешно загружено {created_count} новых товаров!'))