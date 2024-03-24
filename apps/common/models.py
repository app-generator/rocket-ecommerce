from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django_quill.fields import QuillField
from autoslug import AutoSlugField
from django.urls import reverse

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(BaseModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

class ProductStripe(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='stripe_product', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Color(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(BaseModel):
    product_stripe = models.OneToOneField(ProductStripe, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    img_main = models.ImageField(upload_to='product', null=True, blank=True)
    img_1 = models.ImageField(upload_to='product', null=True, blank=True)
    img_2 = models.ImageField(upload_to='product', null=True, blank=True)
    img_3 = models.ImageField(upload_to='product', null=True, blank=True)
    img_4 = models.ImageField(upload_to='product', null=True, blank=True)
    img_5 = models.ImageField(upload_to='product', null=True, blank=True)
    url_video = models.URLField(null=True, blank=True)
    short_description = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def discounted_price(self):
        return round(self.price + (self.price * (self.discount / 100)), 2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'slug': self.slug})




class Cart(BaseModel):
    color = models.ForeignKey(Color, on_delete = models.CASCADE, blank=True,null=True)
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



class ProductProps(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_props")
    prop = models.CharField(max_length=255)
    value = models.CharField(max_length=255)



class TypeChocies(models.TextChoices):
    site_name = 'site_name', 'Site name'
    copyright = 'copyright', 'Copyright'
    stripe_pub_key = 'stripe_pub_key', 'Stripe publishable key'
    stripe_sec_key = 'stripe_sec_key', 'Stripe secret key'
    social_twitter = 'social_twitter', 'Social twitter'
    social_instagram = 'social_instagram', 'Social instagram'
    social_github = 'social_github', 'Social github'
    social_facebook = 'social_facebook', 'Social facebook'
    legal_privacy = 'legal_privacy', 'Legal privacy'
    legal_terms = 'legal_terms', 'Legal terms'
    legal_help = 'legal_help', 'Legal help'
    hero_video = 'hero_video', 'Hero video'

class Settings(BaseModel):
    type = models.CharField(max_length=255, choices=TypeChocies.choices, unique=True)
    value = models.TextField(null=True, blank=True)
    value_html = QuillField(null=True, blank=True)
    file = models.FileField(upload_to='hero/', null=True, blank=True)