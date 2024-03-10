import stripe
import requests
from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from django.conf import settings
from apps.common.models import ProductStripe, Product, Cart, StripeCredentials
from home.forms import ProductForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files import File


def get_stripe_secret_key(request):
  try:
    return StripeCredentials.objects.get(user=request.user).secret_key
  except StripeCredentials.DoesNotExist:
    return getattr(settings, 'STRIPE_SECRET_KEY', None)

# stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY')

from .models import *

def index(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)


def load_stripe_products(request):
  stripe.api_key = get_stripe_secret_key(request)
  stripe_products = stripe.Product.list(expand=['data.default_price'])
  for stripe_product in stripe_products:
    product, created = ProductStripe.objects.update_or_create(
      name=stripe_product['name'],
      defaults={
        'description': stripe_product["description"],
        'price': stripe_product["default_price"]["unit_amount"]/100
      }
    )

    if stripe_product['images']:
      product.image = stripe_product['images'][0]
    
    product.save()

  return redirect(request.META.get('HTTP_REFERER'))


def load_products(request):
  context = {
    'stripe_products': ProductStripe.objects.all(),
    'products': Product.objects.all()
  }
  return render(request, "pages/load_products.html", context)


def create_related_product(request, stripe_product_id):
  stripe_product = get_object_or_404(ProductStripe, pk=stripe_product_id)
  if stripe_product_id:
    product = Product.objects.create(
      product_stripe=stripe_product,
      name=stripe_product.name,
      price=stripe_product.price,
      description=stripe_product.description
    )

    if stripe_product.image:
      response = requests.get(stripe_product.image)
      if response.status_code == 200:
        product.img_main.save(f"{stripe_product_id}_image.jpg", ContentFile(response.content))
      
  return redirect(request.META.get('HTTP_REFERER'))


def edit_product(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  form = ProductForm(instance=product)

  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
      form.save()
      return redirect(reverse('load_products'))
  
  context = {
    'form': form,
    'product': product
  }
  return render(request, 'pages/edit-product.html', context)


def delete_product(request, id):
  product = get_object_or_404(Product, id=id)
  product.delete()
  return redirect(reverse('load_products'))


def product_details(request, product_id):
  product = get_object_or_404(Product, pk=product_id)

  context = {
    'product': product
  }
  return render(request, 'pages/product-details.html', context)


@login_required(login_url='/users/signin/')
def add_to_cart(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  
  cart, created = Cart.objects.get_or_create(
    product=product,
    user=request.user
  )

  if not created:
    cart.quantity += 1
    cart.save()
  
  return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def cart_list(request):
  carts = Cart.objects.filter(user=request.user)

  context = {
    'carts': carts
  }
  return render(request, 'pages/cart-list.html', context)


@login_required(login_url='/users/signin/')
def delete_cart(request, cart_id):
  cart = get_object_or_404(Cart, pk=cart_id)
  cart.delete()
  return redirect(request.META.get('HTTP_REFERER'))


def increment_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))

def decrement_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/users/signin/')
def create_checkout_session(request):
    stripe.api_key = get_stripe_secret_key(request)

    carts = Cart.objects.filter(user=request.user)
    line_items = []

    for cart in carts:
        line_items.append({
            'price_data': {
                'currency': 'usd',  
                'product_data': {
                    'name': cart.product.name,
                },
                'unit_amount': int(cart.product.price * 100), 
            },
            'quantity': cart.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return redirect(session.url)


@login_required(login_url='/users/signin/')
def add_stripe_credentials(request):
  if request.method == 'POST':
    StripeCredentials.objects.update_or_create(
      user=request.user,
      defaults={
        'publishable_key': request.POST.get('publishable_key'),
        'secret_key': request.POST.get('secret_key')
      }
    )
  return redirect(request.META.get('HTTP_REFERER'))