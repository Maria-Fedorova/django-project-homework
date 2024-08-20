from django.urls import path
# from django.contrib import admin
from catalog.apps import CatalogConfig
from catalog.views import contacts, product_list, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    # path("", home, name="home"),
    path("", product_list, name="product_list"),
    path("product/<int:pk>", product_detail, name="product_detail"),
    path("contacts/", contacts, name="contacts"),
]
