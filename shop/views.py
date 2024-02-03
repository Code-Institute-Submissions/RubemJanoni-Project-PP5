
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from myecommerce.forms import LoginForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from .models import Order, CartItem, Cart, Payment, OrderItem, Category, Product
from django.views.generic import TemplateView
from django.core.paginator import Paginator


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

    if request.method == 'GET':
        # Obter o valor selecionado no campo 'size' do formulário
        selected_size = request.GET.get('size')

        # Verificar se o tamanho selecionado é válido
        if selected_size in dict(CartItem.SIZE_CHOICES).keys():
            # Verifica se o produto já está no carrinho, note que ele usa a variável cart que foi validade lá encima e também
            # usa a variavel product que validamos com get_list_or_404
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product )

            # Se o item ja existir, aumenta a quantidade: caso contrário, cria um novo item no carrinho
            if not item_created:
                cart_item.quantity +=1
                cart_item.save()

            # Agora é a vez de atribuir o tamanho selecionado ao campo 'size' do objeto CartItem
            cart_item.size = selected_size
            cart_item.save()


            # Atualiza o número de itens no carrinho na sessão do usuário
            request.session['cart_items'] = CartItem.objects.filter(cart=cart, is_purchased=False).count()

            # Converte o QuerySet para uma lista antes de calcular o valor total do carrinho
            cart_items = list(cart.cartitem_set.all())
            
            # Calcula o valor total do carrinho e converte para float antes de armazenar na sessão
            cart_total = round(sum(float(item.product.price) * item.quantity for item in cart_items),3)
            
            request.session['cart_total'] = cart_total
            
            messages.success(request, 'Product added successfully.')

    return redirect('home')


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'store/order_purchase.html'
    fields = ['shipping_address', 'billing_address']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupera todos os cart items associados ao usuário logado
        user_cart_items = CartItem.objects.filter(cart__user=self.request.user)

        # Adiciona os cart items ao contexto
        context['orders'] = user_cart_items

        # Calcular a soma de todos os itens no carrinho
        context['total_items'] = sum(cart_item.quantity for cart_item in user_cart_items)

        # Calcular o valor total da ordem
        context['total_price'] = round(sum(float(cart_item.product.price) * cart_item.quantity for cart_item in user_cart_items), 3)

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

        # Chama o método form_valid da superclasse para salvar o objeto Order
        response = super().form_valid(form)

        # Cria automaticamente um Payment associado a este pedido
        payment = Payment.objects.create(
            user=user,
            amount=total_price,
            # stripe_charge_id='',  # so remova o comentário se tiver uma API stripe https://stripe.com/br
        )

        # Associa o Payment criado ao Order
        self.object.payment = payment
        self.object.save()

        # Itera sobre os itens do carrinho e define o campo is_purchased como true
        for cart_item in cart_items:
            cart_item.is_purchased = True
            cart_item.save()

        # Limpa as sessões
        if 'cart_items' in self.request.session:
            del self.request.session['cart_items']

        if 'cart_total' in self.request.session:
            del self.request.session['cart_total']

        # Limpa o carrinho após a criação do pedido
        cart.products.clear()

        # Adiciona uma mensagem de sucesso
        messages.success(self.request, 'Pedido criado com sucesso!')

        # O reverse_lazy('nome_da_url') redireciona para a página especificada após a criação do objeto.
        return response

    success_url = reverse_lazy('order_list')


class CartView(View):
    template_name = 'store/cart.html'

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart__user = request.user,  is_purchased=False)
        context = {'cart_items': cart_items}

        return render(request, self.template_name, context)
    
    
class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = 'store/cart_item_confirm_delete.html'  # Crie este template conforme necessário

    def get_success_url(self):
        return reverse_lazy('cart')  # Substitua pelo nome real da sua URL para o carrinho

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Item removido do carrinho com sucesso!')
        return super().delete(request, *args, **kwargs)
    
    
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


# PRODUCT MANAGEMENT category ------------------------------

class CategoryListView(ListView):
    model = Category
    template_name = 'management/category_list.html' 
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'management/category_detail.html' 
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'management/category_form.html' 
    fields = ['name', 'friendly_name']
    success_url = reverse_lazy('home_management') 

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'management/category_form.html' 
    fields = ['name', 'friendly_name']
    success_url = reverse_lazy('home_management') 

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'management/category_confirm_delete.html' 
    success_url = reverse_lazy('home_management') 

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)
    

# PRODUCT MANAGEMENT product ------------------------------
    
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html' 
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html' 
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/product_form.html'  
    fields = ['category', 'sku', 'name', 'description', 'price', 'rating', 'image_url', 'image']
    success_url = reverse_lazy('home_management')  

    def form_valid(self, form):
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/product_form.html'  
    fields = ['category', 'sku', 'name', 'description', 'price', 'rating', 'image_url', 'image']
    success_url = reverse_lazy('home_management')  

    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'  
    success_url = reverse_lazy('home_management')  

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)
    

class HomeView_management(TemplateView):
    template_name = 'home_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginação para Categorias
        categories_list = Category.objects.all()
        categories_paginator = Paginator(categories_list, 10)
        categories_page = self.request.GET.get('categories_page', 1)
        context['categories'] = categories_paginator.get_page(categories_page)

        # Paginação para Produtos
        products_list = Product.objects.all()
        products_paginator = Paginator(products_list, 3)
        products_page = self.request.GET.get('products_page', 1)
        context['products'] = products_paginator.get_page(products_page)

        return context


