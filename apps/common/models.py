from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProductStripe(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='stripe_product', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Product(BaseModel):
    product_stripe = models.OneToOneField(ProductStripe, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=255)
    img_main = models.ImageField(upload_to='product', null=True, blank=True)
    img_1 = models.ImageField(upload_to='product', null=True, blank=True)
    img_2 = models.ImageField(upload_to='product', null=True, blank=True)
    img_3 = models.ImageField(upload_to='product', null=True, blank=True)
    img_4 = models.ImageField(upload_to='product', null=True, blank=True)
    img_5 = models.ImageField(upload_to='product', null=True, blank=True)
    short_description = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def discounted_price(self):
        return self.price + (self.price * (self.discount / 100))

    def __str__(self):
        return self.name



class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    @property
    def total_price(self):
        if self.product.discount:
            discounted_price = self.product.discounted_price()
            return (discounted_price * self.quantity).quantize(Decimal('0.00'))
        else:
            return (self.product.price * self.quantity).quantize(Decimal('0.00'))
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    created_at = models.DateTimeField(auto_now_add=True, null = True, blank=True)

    class Meta:
        ordering = ['-created_at']
    
    def total_order(self):
        total_price = Decimal('0')
        for cart in self.cart.all():
            total_price += cart.total_price
        return total_price.quantize(Decimal('0.00'))
    


class StripeCredentials(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    publishable_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)

# class ProductImage(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product')


