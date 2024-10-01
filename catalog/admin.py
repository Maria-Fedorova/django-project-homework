from django.contrib import admin
from catalog.models import Product, Category, Blog


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description", "price", "category__id")


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    list_display = ("id", "title", 'description', 'created_at', 'is_published')
    ist_filter = ('title',)
    search_fields = ('title', 'description',)
