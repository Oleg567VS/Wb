from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:product_id>/", views.product_details, name="product_details"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
    path("cart/change-quantity/<int:item_id>/", views.cart_change_quantity, name="cart_change_quantity"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),
    path("register/", views.register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("order/create/", views.order_create, name="order_create"),
    path("cart/add-ajax/<int:product_id>/", views.cart_add_ajax, name="cart_add_ajax"),
    path("order/checkout/", views.order_checkout, name="order_checkout"),
]