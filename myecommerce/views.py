
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ContactForm, LoginForm
from shop.models import Product, Address, Payment
from django.contrib import messages
from django.views.decorators.http import require_POST

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import AddressForm 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
import csv




def home_page(request):
    return render(request, "home.html", {'product':Product.objects.all()})


def about_page(request):
    return render(request, "about.html")

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import ContactForm




def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            EmailMessage(
                'Contact Form Submission from {}'.format(name),
                message,
                'form-response@example.com',  # Send from (your website)
                ['rubemjanoni@gmail.com'],  # Send to (your admin email)
                [],
                reply_to=[email]  # Email from the form to get back to
            ).send()

            return redirect('message_success')
    else:
        form = ContactForm()

    context = {
        'title': "Contact 🍕📞",
        'content': "La MAMMA - The best pizza near you...",
        'form': form
    }
    return render(request, 'contact.html', context)

def contact_success(request):
    return render(request, 'message_success.html')




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


class RegisterView(CreateView, SuccessMessageMixin):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/register.html'  # Substitua com o seu template
    success_url = reverse_lazy('home')  # Substitua com a sua URL de sucesso


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
class UserProfileView(DetailView):
    """
    View for displaying user profile information.

    - Shows user details.
    - Retrieves the user's address assuming there is only one address per user.
    """
    model = User
    template_name = 'management/profile_user.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('pk')
        
        # Obtenha o usuário
        user = get_object_or_404(User, pk=username)
        context['user_profile'] = user

        # Obtenha o endereço do usuário (assumindo que há apenas um endereço por usuário)
        address = Address.objects.filter(user=user).first()
        context['user_address'] = address

        return context


# ADDRESS USER -----------------------------------------------------
class AddressCreateView(LoginRequiredMixin,CreateView, SuccessMessageMixin):
    """
    View for creating a new user address.

    - Requires login.
    - Uses the AddressForm for data input.
    - Redirects to the user profile page upon successful creation.
    """
    model = Address
    form_class = AddressForm
    template_name = 'management/profile_user.html'
    success_message = "Address successfully created."
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        user_id = self.request.user.id
        self.success_url = reverse_lazy('user-profile', kwargs={'pk': user_id})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Create'
        return context



class AddressUpdateView(LoginRequiredMixin,UpdateView, SuccessMessageMixin):
    model = Address
    form_class = AddressForm
    template_name = 'management/profile_user.html'
    success_url = reverse_lazy('address-update')  
    success_message = "Address successfully updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Update'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        user_id = self.request.user.id
        self.success_url = reverse_lazy('user-profile', kwargs={'pk': user_id})
        return super().form_valid(form)
    

class AddressDeleteView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):

    """
    Delete address
    """
    model = Address
    template_name = 'management/profile_user.html'
    success_message = "Address successfully deleted."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Delete'
        return context
    
    def form_valid(self, form):
        user_id = self.request.user.id
        self.success_url = reverse_lazy('user-profile', kwargs={'pk': user_id})
        return super().form_valid(form)
    

