from django.contrib import admin

from .models import Product, Category, Brand


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name", )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name", )}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
# Register your models here.
