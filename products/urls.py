from django.urls import path
from .views import (
    ListCategories,
    ListProducts,
    ProductDetail,
    AddCategory,
    AddProduct,
)

urlpatterns = [
    path("categories/", ListCategories.as_view(), name="list_categories"),
    path("products/", ListProducts.as_view(), name="list_products"),
    path("products/<int:product_id>/", ProductDetail.as_view(), name="product_detail"),
    path("categories/add/", AddCategory.as_view(), name="add_category"),
    path("products/add/", AddProduct.as_view(), name="add_product"),
]
