import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from apps.common.models import Product, ProductImage

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY')

from .models import *

def index(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)


def load_stripe_products(request):
  stripe_products = stripe.Product.list(expand=['data.default_price'])
  for stripe_product in stripe_products:
    product = Product.objects.create(
      title=stripe_product['name'],
      short_description=stripe_product["description"][:100] if stripe_product["description"] else '',
      full_description=stripe_product["description"],
      price=stripe_product["default_price"]["unit_amount"]/100,
    )

    for image in stripe_product['images']:
      product_image = ProductImage.objects.create(
        product=product,
        image=image
      )

  return redirect(request.META.get('HTTP_REFERER'))


def starter(request):

  context = {}
  return render(request, "pages/starter.html", context)