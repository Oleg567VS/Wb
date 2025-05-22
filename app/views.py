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
from .models import Product, Cart, CartItem, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        if carts.count() > 1:
            # Оставить одну, остальные удалить
            main_cart = carts.first()
            for c in carts[1:]:
                c.delete()
            cart = main_cart
            created = False
        elif carts.exists():
            cart = carts.first()
            created = False
        else:
            cart = Cart.objects.create(user=request.user)
            created = True
    else:
        session_key = request.session.session_key or request.session.create()
        carts = Cart.objects.filter(session_key=session_key, user__isnull=True)
        if carts.count() > 1:
            main_cart = carts.first()
            for c in carts[1:]:
                c.delete()
            cart = main_cart
            created = False
        elif carts.exists():
            cart = carts.first()
            created = False
        else:
            cart = Cart.objects.create(session_key=session_key)
            created = True
    return cart

def index(request):
    products_list = Product.objects.all().order_by('id')
    paginator = Paginator(products_list, 10)
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

@csrf_exempt
def cart_change_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=_get_or_create_cart(request))
    quantity = request.POST.get('quantity')
    if quantity and quantity.isdigit():
        cart_item.quantity = int(quantity)
        if cart_item.quantity > 0:
            cart_item.save()
        else:
            cart_item.delete()
    # AJAX: вернуть новую сумму и итог
    cart = cart_item.cart
    return JsonResponse({
        'item_total': cart_item.item_total if cart_item.id else 0,
        'cart_total': cart.total_price
    })

def cart_clear(request):
    cart = _get_or_create_cart(request)
    cart.items.all().delete()  # Удаляем все элементы корзины
    return redirect('cart_detail')

@login_required
def order_create(request):
    cart = _get_or_create_cart(request)
    if cart.items.exists():
        cart.items.all().delete()
        messages.success(request, "Ваш заказ успешно оформлен!")
    else:
        messages.warning(request, "Корзина пуста.")
    return redirect('cart_detail')

@login_required
def order_checkout(request):
    if not request.user.is_authenticated:
        # Перенаправить на страницу входа, после входа вернуть в корзину
        return redirect(f"{reverse('login')}?next={reverse('cart_detail')}")
    cart = _get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Корзина пуста.")
        return redirect('cart_detail')
    if request.method == "POST":
        cart.items.all().delete()
        messages.success(request, "Ваш заказ успешно оформлен!")
        return redirect('index')
    return render(request, 'app/order_checkout.html', {'cart': cart})

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False, label="Телефон")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("phone_number",)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Перенос корзины после регистрации
            _merge_guest_cart(request, user)
            auth_login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "app/register.html", {"form": form})

from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    template_name = "app/login.html"
    def form_valid(self, form):
        response = super().form_valid(form)
        _merge_guest_cart(self.request, self.request.user)
        return response

def _merge_guest_cart(request, user):
    session_key = request.session.session_key
    if not session_key:
        return
    try:
        guest_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user)
    for item in guest_cart.items.all():
        user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
        if not created:
            user_item.quantity += item.quantity
            user_item.save()
        else:
            user_item.quantity = item.quantity
            user_item.save()
    guest_cart.delete()

def cart_context(request):
    from .models import Cart
    cart = None
    cart_total_quantity = 0
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        if carts.count() > 1:
            main_cart = carts.first()
            for c in carts[1:]:
                c.delete()
            cart = main_cart
        elif carts.exists():
            cart = carts.first()
        else:
            cart = Cart.objects.create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        carts = Cart.objects.filter(session_key=session_key, user__isnull=True)
        if carts.count() > 1:
            main_cart = carts.first()
            for c in carts[1:]:
                c.delete()
            cart = main_cart
        elif carts.exists():
            cart = carts.first()
        else:
            cart = Cart.objects.create(session_key=session_key)
    if cart:
        cart_total_quantity = sum(item.quantity for item in cart.items.all())
    return {'cart': cart, 'cart_total_quantity': cart_total_quantity}

@require_POST
def cart_add_ajax(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart_count = cart.items.count()
    cart_total = cart.total_price
    cart_total_quantity = sum(item.quantity for item in cart.items.all())
    return JsonResponse({
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_total_quantity': cart_total_quantity,
        'item_id': cart_item.id,
        'item_quantity': cart_item.quantity
    })

# Create your views here.
