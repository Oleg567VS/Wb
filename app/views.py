from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product

def index(request):
    # Получаем все продукты
    products_list = Product.objects.all()
    
    # Создаем пагинатор - 12 товаров на страницу
    paginator = Paginator(products_list, 12)
    
    # Получаем номер страницы из GET-параметра
    page = request.GET.get('page')
    
    try:
        # Получаем объекты для запрошенной страницы
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если page не целое число, показываем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если page вне диапазона (например, 9999), показываем последнюю страницу
        products = paginator.page(paginator.num_pages)
    
    context = {"products": products}
    return render(request, "app/index.html", context)

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = []
    categories.append(product.category)
    cur_category = product.category
    while cur_category.parent:
        categories.append(cur_category.parent)
        cur_category = cur_category.parent
    categories.reverse()
    context = {"product": product, "categories": categories}
    return render(request, "app/product_details.html", context)

# Create your views here.
