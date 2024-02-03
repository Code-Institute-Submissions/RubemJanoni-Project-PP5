from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
    

class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]
    size = models.CharField(
        max_length=10, choices=SIZE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    # Ligaçaõ do usuario associado ao carrinho
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # Produtos para serem adicionados ao carrinho 
    products = models.ManyToManyField(Product, through="CartItem")

    def __str__(self):
        return f'Cart - {self.user.username}'


class CartItem(models.Model):
    # Nome do produto adicionado ao carrinho
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Ligação da quantidade de cada item no carrinho
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # Numero de unidades do pedido
    quantity = models.PositiveBigIntegerField(default=1)
    # Booleano com padrão False
    is_purchased = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart'
    

class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name_plural = 'Addresses'



class Payment(models.Model):
    # Se tiver uma API stripe, (https://stripe.com/br) remova o comentário do campo 'stripe_charge_id' e faça as migrações
    #stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in order'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Order - {self.user.username} - {self.order_date}'


# Adiciona itens do carrinho ao pedido após a criação do pedido
@receiver(post_save, sender=Order)
def add_cart_items_to_order(sender, instance, created, **kwargs):
    if created:
        cart_items = CartItem.objects.filter(cart__user=instance.user, is_purchased=False)

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                product=cart_item.product,
                quantity=cart_item.quantity,
                is_purchased=True
            )
            instance.items.add(order_item)

        # Limpa os itens do carrinho após adicioná-los ao pedido
        cart_items.update(is_purchased=True)
        cart_items.delete()

