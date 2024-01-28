from django.contrib import admin
from django.urls import path, include
from .views import home_page, about_page, contact_page

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),     
    path('accounts/', include('allauth.urls')),

    # Abaixo, url do shop
    path('shop/', include('shop.urls')),
    
]



