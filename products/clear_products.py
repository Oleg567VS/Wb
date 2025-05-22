from app.models import Product, Brand, Category

Product.objects.all().delete()
Brand.objects.all().delete()
Category.objects.all().delete()
print('Все товары, бренды и категории удалены!') 