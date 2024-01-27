# store/urls.py
from django.urls import path
from .views import add_to_cart, CartView, ProductListView, OrderListView, Produto_Detail, OrderCreateView
from myecommerce.views import login_in_detailview


urlpatterns = [
    path('product/<int:pk>/', Produto_Detail.as_view(), name='product'),
    path('login/', login_in_detailview, name='login_view'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    
]
