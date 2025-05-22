from app.models import Category, Brand, Product

# Категории
categories = [
    'Смартфоны', 'Ноутбуки', 'Планшеты', 'Аксессуары', 'Телевизоры',
    'Наушники', 'Умные часы', 'Фотоаппараты', 'Игровые приставки', 'Мониторы',
    'Принтеры', 'Сканеры', 'Клавиатуры', 'Мыши', 'Колонки',
    'Сетевое оборудование', 'Внешние диски', 'SSD', 'Видеокарты', 'Процессоры',
    'Материнские платы', 'Оперативная память', 'Корпуса ПК'
]

# Бренды
brands = [
    'Apple', 'Samsung', 'Xiaomi', 'Sony', 'HP', 'Dell', 'Lenovo', 'Asus', 'Acer', 'Canon',
    'Nikon', 'Microsoft', 'Logitech', 'Kingston', 'Corsair', 'MSI', 'Gigabyte', 'AMD', 'Intel', 'Philips',
    'JBL', 'Huawei', 'TP-Link'
]

category_objs = []
brand_objs = []

for name in categories:
    obj, _ = Category.objects.get_or_create(name=name)
    category_objs.append(obj)

for name in brands:
    obj, _ = Brand.objects.get_or_create(name=name, site_url=f'https://{name.lower()}.com', country='США')
    brand_objs.append(obj)

for i in range(23):
    Product.objects.create(
        name=f'Товар {i+1}',
        desc=f'Описание для товара {i+1}',
        price=1000 + i*100,
        image='products/default.jpg',
        category=category_objs[i],
        brand=brand_objs[i],
        slug=f'product-{i+1}'
    )
print('Готово: 23 товара, категории и бренды созданы!') 