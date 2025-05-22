from django.contrib import admin

from .models import Product, Category, Brand, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name", )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name", )}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(User, BaseUserAdmin)
# Register your models here.
