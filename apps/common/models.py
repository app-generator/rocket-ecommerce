from django.db import models
from django.contrib.auth.models import User

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
    image = models.URLField(null=True, blank=True)
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
    promo = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity


# class ProductImage(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product')
