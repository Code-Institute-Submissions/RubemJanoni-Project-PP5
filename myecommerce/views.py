from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import ContactForm, LoginForm, RegisterForm
from shop.models import Product
from django.contrib import messages
from django.contrib.auth.views import LoginView
from allauth.account.views import SignupView



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

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST


@require_POST
def login_in_detailview(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    next_url = request.POST.get('next', '/')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(self.request, 'Login bem-sucedido.')
        return redirect(next_url)
    else:
        messages.error(self.request, 'Credenciais inválidas.')
        return redirect('login')


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
            
            messages.success(request, 'Login bem-sucedido.')
            return redirect('/')

        else:
            print('invalid login')
    return render(request, 'auth/login.html', context)


User = get_user_model()

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import AddressForm 
from shop.models import Address
from django.urls import reverse_lazy

class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/register.html'  
    success_url = reverse_lazy('login')  


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. Please login.')
        return response

    def dispatch(self, request, *args, **kwargs):
        # Redireciona usuários já autenticados para a página inicial
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)



def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

# INFO USER
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from shop.models import  Address

class UserProfileView(DetailView):
    model = User
    template_name = 'auth/perfilUser.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        
        # Obtenha o usuário
        user = get_object_or_404(User, username=username)
        context['user_profile'] = user

        # Obtenha o endereço do usuário (assumindo que há apenas um endereço por usuário)
        address = Address.objects.filter(user=user).first()
        context['user_address'] = address

        return context


# ADDRESS USER -----------------------------------------------------

class AddressCreateView(CreateView, ListView):
    model = Address
    form_class = AddressForm
    template_name = 'auth/perfilUser.html'
    success_url = reverse_lazy('address-create')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Create'
        return context



class AddressUpdateView(UpdateView, ListView):
    model = Address
    form_class = AddressForm
    template_name = 'auth/perfilUser.html'
    success_url = reverse_lazy('address-update')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Update'
        return context

    

class AddressDeleteView(DeleteView, ListView):
    model = Address
    template_name = 'auth/perfilUser.html'
    success_url = reverse_lazy('address-delete')  

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Delete'
        return context






