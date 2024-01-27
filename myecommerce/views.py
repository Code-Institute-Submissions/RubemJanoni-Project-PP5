from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import ContactForm, LoginForm, RegisterForm
from shop.models import Product
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST


def home_page(request):
    """
    render homepage displaying all products
    """
    return render(request, "home.html", {'product':Product.objects.all()})


def about_page(request):
    """
    render about page displaying all products
    """
    return render(request, "about.html")


def contact_page(request):
    """
    Renders the contact page, allowing you to send messages.
    """
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': "Contact 🍕📞",
        'content': "La MAMMA - The best pizza near you...",
        'form': contact_form
    }
    if request.method == 'POST':
        print(request.POST)

    return render(request, "contact.html", context)




@require_POST
def login_in_detailview(request):
    """
    Make login and redirect next page.
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    next_url = request.POST.get('next', '/')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, 'Login bem-sucedido.')
        return redirect(next_url)
    else:
        messages.error(request, 'Credenciais inválidas.')
        return redirect('login')


def login_page(request):
    """
    Renders the login page and performs user authentication.
    """
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

        try:

            new_user = User.objects.create_user(username, email, password)
            messages.success(request, 'Account created successfully. Please login.')
            print(new_user)
            return redirect('login_page')                  
                
               

        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            print(f"Error creating user: {e}")           
            
       

        return render(request, "auth/register.html", context)




def logout_page(request):
    """
    Realiza o logout do usuário e redireciona para a página de login.
    """
    logout(request)
    return redirect('login')