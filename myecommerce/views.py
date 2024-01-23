from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import ContactForm, LoginForm, RegisterForm
from shop.models import Product
from django.contrib import messages



def home_page(request):
    return render(request, "home.html", {'product':Product.objects.all()})


def about_page(request):
    return render(request, "about.html")


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "Contact 🍕📞",
        'content': "La MAMMA - The best pizza near you...",
        'form': contact_form
    }
    if request.method == 'POST':
        print(request.POST)

    return render(request, "contact.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print('User logged in')
    print(request.user.is_authenticated)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        print(request.user.is_authenticated)

        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            print('Valid login')
            print(request.user.is_authenticated)
            return redirect('/')

        else:
            print('invalid login')
    return render(request, 'auth/login.html', context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)

        print(new_user)

    return render(request, "auth/register.html", context)

        


def logout_page(request):
    logout(request)
    return redirect('login')





