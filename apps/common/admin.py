from django.contrib import admin

from django.apps import apps
from django.contrib import admin

# from apps.common.models import Product, ProductImage

# Register your models here.

app_models = apps.get_app_config('common').get_models()
for model in app_models:
    try:    
 
        admin.site.register(model)

    except Exception:
        pass


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price', 'featured', 'stock', )
#     inlines = [
#         ProductImageInline,
#     ]