from django.urls import path
from .views import add_to_cart, view_cart, checkout, order_history

urlpatterns = [
    path("add/", add_to_cart, name="add_to_cart"),
    path("view/", view_cart, name="view_cart"),
    path("checkout/", checkout, name="checkout"),
    path("orders/", order_history, name="order_history"),
]
