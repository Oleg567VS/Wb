from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<int:product_id>/", views.product_details, name="product_details"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
    path("cart/change-quantity/<int:item_id>/", views.cart_change_quantity, name="cart_change_quantity"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),
]