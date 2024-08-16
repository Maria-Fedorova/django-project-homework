from django.contrib import admin
from catalog.models import Product, Category


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description", "price", "category__id")


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name")
