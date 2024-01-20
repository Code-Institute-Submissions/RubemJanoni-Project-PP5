from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
"""
# Para usar LoginView é preciso "from django.contrib.auth.views import LoginView"
class Make_login (LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        # Para usar reverse_lazy é preciso "from django.urls import reverse_lazy"
        return reverse_lazy('shop:List_publication')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Para usar messages é preciso "from django.contrib import messages "
        messages.success(self.request, 'Login successfully. Welcome!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Something is wrong, Try again.')
        return response

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Para usar redirect é preciso " from django.shortcuts import redirect "
            return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)
    """

# ########################################################
from django.views import View
from .models import CartItem, Product, Order, Cart
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    # Verifica se o produto existe, validando com o get_object_or_404
    product = get_object_or_404(Product, id = product_id)
    
    # Verifica se o usuário ja tem um carrinho, get_or_create verifica se há algum produto (objeto) no carrinho
    # se não existir ele retorna uma tupla com dois valores: um objeto e um booleano que pode ser True ou False
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Verifica se o produto já está no carrinho, note que ele usa a variável cart que foi validade lá encima e também
    # usa a variavel product que validamos com get_list_or_404
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product )

    # Se o item ja existir, aumenta a quantidade: caso contrário, cria um novo item no carrinho
    if not item_created:
        cart_item.quantity +=1
        cart_item.save()

    return redirect('home')


class CartView(View):
    template_name = 'store/cart.html'

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart__user = request.user)
        context = {'cart_items': cart_items}

        return render(request, self.template_name, context)
    

class ProductListView(View):
    template_name = 'store/product_list.html'

    def get(self, request, *args, **kwargs):
        products = Product. objects.all()
        context = {'products': products}

        return render(request, self.template_name, context)
    

class OrderListView(View):
    template_name = 'store/order_list.html'
    
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user = request.user)
        context = {'orders': orders}

        return render(request, self.template_name, context)

