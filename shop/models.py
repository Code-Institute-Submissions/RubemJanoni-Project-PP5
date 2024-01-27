from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


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

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):

    """
    Class payment

    """
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    
class Order(models.Model):
    


