from django.urls import path
from .views import list_categories, list_products, product_detail, add_category, add_product

urlpatterns = [
    path("categories/", list_categories, name="list_categories"),
    path("categories/add/", add_category, name="add_category"),
    path("products/", list_products, name="list_products"),
    path("products/add/", add_product, name="add_product"),
    path("products/<int:product_id>/", product_detail, name="product_detail"),
]
