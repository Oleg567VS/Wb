from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        "URL", max_length=250, unique=True, null=True, editable=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    site_url = models.URLField(
        verbose_name="Ссылка на сайт",
        max_length=200,
    )

    country = models.CharField(
        verbose_name="Страна",
        max_length=200,
    )

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        verbose_name="Наименование",
        max_length=200,
    )
    desc = models.TextField(
        verbose_name="Описание",
        max_length=3000,
    )

    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=10,
        decimal_places=2,
    )

    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="products/",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name="Бренд",
        on_delete=models.CASCADE,
    )

    slug = models.SlugField(
        "URL", max_length=250, unique=True, null=True, editable=True
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    session_key = models.CharField(
        max_length=40,
        verbose_name="Ключ сессии",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        if self.user:
            return f"Корзина пользователя {self.user}"
        else:
            return f"Гостевая корзина ({self.session_key})"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name="Корзина",
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def item_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
    #brand   
    #name  
    #category
    #desc
    #image 


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

# Create your models here.
