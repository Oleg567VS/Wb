#from django.shortcuts import render
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from .models import Product

#def index(request):
    # Получаем все продукты
   # products_list = Product.objects.all()
    
    # Создаем пагинатор - 12 товаров на страницу
   # paginator = Paginator(products_list, 12)
    
    # Получаем номер страницы из GET-параметра
   # page = request.GET.get('page')
    
   # try:
        # Получаем объекты для запрошенной страницы
      #  products = paginator.page(page)
  #  except PageNotAnInteger:
        # Если page не целое число, показываем первую страницу
       # products = paginator.page(1)
   # except EmptyPage:
        # Если page вне диапазона (например, 9999), показываем последнюю страницу
       # products = paginator.page(paginator.num_pages)
    
   # context = {"products": products}
  #  return render(request, "app/index.html", context)

#def product_details(request, product_id):
   # product = Product.objects.get(id=product_id)
   # categories = []
   # categories.append(product.category)
   # cur_category = product.category
  #  while cur_category.parent:
      #  categories.append(cur_category.parent)
      #  cur_category = cur_category.parent
  #  categories.reverse()
  #  context = {"product": product, "categories": categories}
   # return render(request, "app/product_details.html", context)
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def index(request):
    products_list = Product.objects.all().order_by('id')
    paginator = Paginator(products_list, 12)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    page_range = paginator.get_elided_page_range(number=products.number, on_each_side=2, on_ends=1)

    context = {
        "products": products,
        "page_range": page_range
    }
    return render(request, "app/index.html", context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = []
    cur_category = product.category
    while cur_category:
        categories.append(cur_category)
        cur_category = cur_category.parent
    categories.reverse()

    context = {"product": product, "categories": categories}
    return render(request, "app/product_details.html", context)

def cart_detail(request):
    cart = _get_or_create_cart(request)
    return render(request, 'app/cart.html', {'cart': cart})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=_get_or_create_cart(request))
    cart_item.delete()
    return redirect('cart_detail')

def cart_change_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=_get_or_create_cart(request))
    quantity = request.POST.get('quantity')
    if quantity and quantity.isdigit():
        cart_item.quantity = int(quantity)
        if cart_item.quantity > 0:
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_detail')
def cart_clear(request):
    cart = _get_or_create_cart(request)
    cart.items.all().delete()  # Удаляем все элементы корзины
    return redirect('cart_detail')
from django.contrib import messages

def order_create(request):
    cart = _get_or_create_cart(request)

    if cart.items.exists():
        # Очищаем корзину
        cart.items.all().delete()
        
        # Показываем сообщение об успехе
        messages.success(request, "Ваш заказ успешно оформлен!")
    else:
        messages.warning(request, "Корзина пуста.")

    return redirect('index')
# Create your views here.
