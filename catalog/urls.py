from django.urls import path
# from django.contrib import admin
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ContactsPageView

app_name = CatalogConfig.name

urlpatterns = [
    # path("", home, name="home"),
    path("", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("product/create", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("contacts/", ContactsPageView.as_view(), name="contacts"),
    # path("contacts/", contacts, name="contacts"),
]
