# store/urls.py
from django.urls import path
from .views import add_to_cart, CartView, ProductListView, OrderListView


urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    
]
