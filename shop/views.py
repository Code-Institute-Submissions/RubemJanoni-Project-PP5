from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import CartItem, Product, Order, Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from myecommerce.forms import LoginForm
from django.views.generic.edit import CreateView



class Produto_Detail(DetailView):
    model = Product
    template_name = 'store/detail.html'
    context_object_name = 'product'

    # Caso o cliente não esteja logado ao adicionar o produto no carrinho,
    # Será exigido que ele faça login
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login'] = LoginForm()
        return context


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

    # Atualiza o número de itens no carrinho na sessão do usuário
    request.session['cart_items'] = CartItem.objects.filter(cart=cart).count()

    # Converte o QuerySet para uma lista antes de calcular o valor total do carrinho
    cart_items = list(cart.cartitem_set.all())
    
    # Calcula o valor total do carrinho e converte para float antes de armazenar na sessão
    cart_total = round(sum(float(item.product.price) * item.quantity for item in cart_items),3)
    request.session['cart_total'] = cart_total

    return redirect('home')



class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'store/order_purchase.html'
    fields = ['shipping_address', 'billing_address', 'payment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupera todos os cart items associados ao usuário logado
        user_cart_items = CartItem.objects.filter(cart__user=self.request.user)

        # Adiciona os cart items ao contexto
        context['orders'] = user_cart_items

        # Calcular a soma de todos os itens no carrinho
        context['total_items'] = sum(cart_item.quantity for cart_item in user_cart_items)

        # Calcular o valor total da ordem
        context['total_price'] = round(sum(float(cart_item.product.price) * cart_item.quantity for cart_item in user_cart_items),3)


        return context

    def form_valid(self, form):
        # Obtém o usuário atual
        user = self.request.user

        # Obtém o carrinho do usuário
        cart, created = Cart.objects.get_or_create(user=user)

        # Obtém os itens do carrinho do usuário
        cart_items = CartItem.objects.filter(cart=cart)

        # Calcula o total_price com base nos itens do carrinho
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Preenche os campos restantes do formulário
        form.instance.user = user
        form.instance.total_price = total_price
        form.instance.ordered = False  # ou True, dependendo da sua lógica

         # Adiciona uma mensagem de sucesso
        messages.success(self.request, 'Pedido criado com sucesso!')

        # Chama o método form_valid da superclasse para salvar o objeto Order
        return super().form_valid(form)

    # O reverse_lazy('nome_da_url') redireciona para a página especificada após a criação do objeto.
    success_url = reverse_lazy('order_list')





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

