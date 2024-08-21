from django.urls import path
# from django.contrib import admin
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ContactsView, BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, \
    publishing_action

app_name = CatalogConfig.name

urlpatterns = [
    # path("", home, name="home"),
    path("", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("product/create", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("contacts/", ContactsView.as_view(), name="contacts"),

    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/create', BlogCreateView.as_view(), name='blog_create'),
    path('blog/detail/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/update/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),
    path("blog/publishing/<slug:slug>", publishing_action, name="publishing_action"),
    # path("contacts/", contacts, name="contacts"),
]
