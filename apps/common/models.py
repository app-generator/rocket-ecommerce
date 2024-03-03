from django.db import models

# Create your models here.
        

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TagChoices(models.TextChoices):
    SHOES = 'SHOES', 'Shoes'
    CLOTHES = 'CLOTHES', 'Clothes'

class Product(BaseModel):
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=100, null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=50, choices=TagChoices.choices, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField(default=False)
    promo = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product', null=True, blank=True)


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product')