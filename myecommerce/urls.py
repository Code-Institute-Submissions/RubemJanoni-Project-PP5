
from django.contrib import admin
from django.urls import path, include
from .views import home_page, about_page, contact_page,  login_page, logout_page, RegisterView, contact_success


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('contactsuccess/', contact_success, name='message_success'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_page, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('shop/', include('shop.urls')),

    # ERRO 404
    # Adicione a seguinte linha para lidar com o erro 404
    re_path(r'^.*/$', handler404),
    re_path(r'^.*/500/$', handler500)
]
