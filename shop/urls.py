# store/urls.py
from django.urls import path
from .views import add_to_cart, CartView, ProductListView, OrderListView, Produto_Detail, OrderCreateView, CartItemDeleteView, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, HomeView_management

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

    path('management', HomeView_management.as_view(), name='home_management'),

    # CATEGORY
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # PRODUCT
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

]
