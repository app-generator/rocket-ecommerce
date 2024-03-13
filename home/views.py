import stripe
import requests
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponseForbidden
from django.conf import settings
from apps.common.models import ProductStripe, Product, Cart, StripeCredentials, Order , Tag
from home.forms import ProductForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.files.base import ContentFile
from django.core.files import File
from .models import *


def get_stripe_secret_key(request):
  try:
    return StripeCredentials.objects.get(user=request.user).secret_key
  except StripeCredentials.DoesNotExist:
    return getattr(settings, 'STRIPE_SECRET_KEY', None)


def staff_member_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def index(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)


@staff_member_required
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


@staff_member_required
def load_products(request):
  context = {
    'stripe_products': ProductStripe.objects.all(),
    'products': Product.objects.all()
  }
  return render(request, "pages/load_products.html", context)

@staff_member_required
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


@staff_member_required
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

@staff_member_required
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
    user=request.user,
    is_ordered = False,

  )

  if not created:
    cart.quantity += 1
    cart.save()
  
  return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def cart_list(request):
  carts = Cart.objects.filter(user=request.user, is_ordered=False)

  context = {
    'carts': carts
  }
  return render(request, 'pages/cart-list.html', context)


@login_required(login_url='/users/signin/')
def delete_cart(request, cart_id):
  cart = get_object_or_404(Cart, pk=cart_id)
  cart.delete()
  return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def increment_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def decrement_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/users/signin/')
def create_checkout_session(request):
    stripe.api_key = get_stripe_secret_key(request)
    carts = Cart.objects.filter(user=request.user, is_ordered=False)
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
        success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = request.build_absolute_uri(reverse('payment_cancel'))
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

@login_required(login_url='/users/signin/')
def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        # Handle the case when session_id is not provided
        return render(request, 'error.html', {'error_message': 'Invalid session ID'})

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        carts = Cart.objects.filter(user=request.user, is_ordered=False)
        for cart in carts:
            cart.is_ordered = True
            cart.save()
            Order.objects.create(user=request.user, cart=cart)

    # Add any additional logic or redirect here
    return render(request, 'pages/payment-success.html')


@login_required(login_url='/users/signin/')
def payment_cancel(request):
   return render(request, 'pages/payment-cancel.html')



def category_page(request):
   all_products = Product.objects.all()
   tags = Tag.objects.filter(product__in=all_products).values('name').annotate(count=Count('name'))

   context = {
      'tags': tags,
   }
   return render(request,'pages/category-list.html', context)



def category_products(request,name):
    tag = get_object_or_404(Tag , name=name)
    products = tag.product_set.all()


    context = {
        'tag':tag,
        'products': products,
    }
    return render(request, 'pages/category-products.html', context)




def discounted_product_list(request):
    discounted_products = Product.objects.filter(discount__isnull=False)
    context = {
        'products': discounted_products,
    }

    return render(request, 'pages/discounted-product.html', context)



def homepage(request):
    products = Product.objects.all()
    context = {
       'products':products
    }
    return render(request, 'pages/home-page.html',context)



@staff_member_required
@login_required(login_url='/admin/')
def fetch_stripe_transactions(request):
    stripe.api_key = get_stripe_secret_key(request)
    charges = stripe.Charge.list(limit=10, expand=['data.payment_method_details.card'])
    transactions = []
    for charge in charges.data:
        card_number = ''
        if charge.payment_method_details and charge.payment_method_details.type == 'card':
            card_number = charge.payment_method_details.card.last4
        
        transaction = {
            'transaction_number': charge.id,
            'amount': charge.amount / 100,  
            'currency': charge.currency.upper(),
            'card_number': card_number,
            'payment_status': charge.status,
        }
        transactions.append(transaction)

    return render(request, 'pages/transaction.html', {'transactions': transactions})