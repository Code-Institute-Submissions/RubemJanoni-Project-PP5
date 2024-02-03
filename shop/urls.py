# store/urls.py
from django.urls import path
from .views import add_to_cart, CartView, ProductListView, OrderListView, Produto_Detail, OrderCreateView, CartItemDeleteView
from myecommerce.views import login_in_detailview, AddressCreateView, AddressDeleteView, AddressUpdateView, UserProfileView


urlpatterns = [
    path('product/<int:pk>/', Produto_Detail.as_view(), name='product'),
    path('login/', login_in_detailview, name='login_view'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    # Perfil User
    path('user/<int:pk>', UserProfileView.as_view(), name='user-profile'),

    # ADDRESS
    path('address/create', AddressCreateView.as_view(), name='address-create'),
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
    path('address/<int:pk>/update/', AddressUpdateView.as_view(), name='address-update'),
 
]
