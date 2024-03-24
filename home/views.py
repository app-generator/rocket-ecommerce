import stripe
import requests
import base64
from django.db.models import Count, F
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from apps.common.models import ProductStripe, Product, Cart, StripeCredentials, Order , Tag , Color, ProductProps, Settings, TypeChocies
from home.forms import ProductForm, PrivacyPolicyForm, TermsForm, HelpForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.files.base import ContentFile
from django.contrib import messages
from django.core.files import File
from django.core.files.base import ContentFile
from .models import *

def get_stripe_secret_key(request):
  demo_mode = getattr(settings, 'DEMO_MODE')
  if not demo_mode:
    try:
      return StripeCredentials.objects.get(user=request.user).secret_key
    except StripeCredentials.DoesNotExist:
      return getattr(settings, 'STRIPE_SECRET_KEY', None)
  else:
     return getattr(settings, 'STRIPE_SECRET_KEY', None)


def staff_member_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('signin')  
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Dashboard
def dashboard(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)

def homepage(request, slug=None):
  context       = {}
  filter_string = {}

  if slug:
      
    if 'search' == slug:
      return search_page(request)
    else:
      context['tag'] = slug

    tag = Tag.objects.get(slug=slug)
    filter_string['tags__in'] = [tag.pk]
  
  products = Product.objects.filter(**filter_string)
  context['products'] = products
  return render(request, 'pages/home-page.html',context)

def search_page(request):
  context       = {}
  filter_search = {}

  search = request.GET.get('search')
  if search:
    filter_search['name__icontains'] = search
    context['search'] = search
  
  products = Product.objects.filter(**filter_search)
  context['products'] = products
  return render(request, 'pages/search-page.html', context)

@staff_member_required
def load_stripe_products(request):
  stripe.api_key = get_stripe_secret_key(request)
  stripe_products = stripe.Product.list(expand=['data.default_price'], active=True)
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
    'products': Product.objects.all(),
    'demo_mode': getattr(settings, 'DEMO_MODE'),
    'segment': 'product_list',
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
def delete_local_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect(reverse('load_products'))


@staff_member_required
def delete_both_product(request, local_product, stripe_product):
    local_product = get_object_or_404(Product, id=local_product)
    stripe_product = get_object_or_404(ProductStripe, id=stripe_product)
    if local_product:
        local_product.delete()
    if stripe_product:
        stripe_product.delete()
    return redirect(reverse('load_products'))


@staff_member_required
def general_settings(request):
    if request.method == 'POST':
        for attribute, value in request.POST.items():
            if attribute == 'csrfmiddlewaretoken':
                continue
            
            if value:
                Settings.objects.update_or_create(
                    type=TypeChocies[attribute],
                    defaults={
                    'value': value
                    }
                )

        for attribute, value in request.FILES.items():
            if attribute == 'csrfmiddlewaretoken':
                continue
            
            if value:
                Settings.objects.update_or_create(
                    type=TypeChocies[attribute],
                    defaults={
                    'file': value
                    }
                )

        return redirect(request.META.get('HTTP_REFERER'))
    

    context = {
       'parent': 'settings',
       'segment': 'general_settings'
    }
    return render(request, 'pages/settings/general-settings.html', context)


@staff_member_required
@login_required(login_url='/admin/')
def stripe_settings(request):

    context = {
       'parent': 'settings',
       'segment': 'stripe_settings'
    }
    return render(request, 'pages/settings/stripe-settings.html', context)

@staff_member_required
def social_settings(request):
    if request.method == 'POST':
        for attribute, value in request.POST.items():
            if attribute == 'csrfmiddlewaretoken':
                continue
            
            Settings.objects.update_or_create(
                type=TypeChocies[attribute],
                defaults={
                'value': value
                }
            )
        return redirect(request.META.get('HTTP_REFERER'))
    
    context = {
       'parent': 'settings',
       'segment': 'social_settings'
    }
    return render(request, 'pages/settings/social-settings.html', context)


@staff_member_required
def privacy_settings(request):
    legal_privacy = Settings.objects.filter(type='legal_privacy').first()
    initial_data = {
        'legal_privacy': legal_privacy.value_html if legal_privacy else '',
    }
    form = PrivacyPolicyForm(initial=initial_data)

    if request.method == 'POST':
        for attribute, value in request.POST.items():
            if attribute == 'csrfmiddlewaretoken':
                continue
            
            Settings.objects.update_or_create(
                type=TypeChocies[attribute],
                defaults={
                'value_html': value
                }
            )
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
       'form': form,       
       'parent': 'settings',
       'segment': 'privacy_settings'
    }
    return render(request, 'pages/settings/privacy-settings.html', context)

@staff_member_required
def terms_settings(request):
    legal_terms = Settings.objects.filter(type='legal_terms').first()
    initial_data = {
        'legal_terms': legal_terms.value_html if legal_terms else '',
    }
    form = TermsForm(initial=initial_data)

    if request.method == 'POST':
        for attribute, value in request.POST.items():
            if attribute == 'csrfmiddlewaretoken':
                continue
            
            Settings.objects.update_or_create(
                type=TypeChocies[attribute],
                defaults={
                'value_html': value
                }
            )
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
       'form': form,       
       'parent': 'settings',
       'segment': 'terms_settings'
    }
    return render(request, 'pages/settings/terms-settings.html', context)


@staff_member_required
def help_settings(request):
    legal_help = Settings.objects.filter(type='legal_help').first()
    initial_data = {
        'legal_help': legal_help.value_html if legal_help else '',
    }
    form = HelpForm(initial=initial_data)

    if request.method == 'POST':
        for attribute, value in request.POST.items():
            if attribute == 'csrfmiddlewaretoken':
                continue
            
            Settings.objects.update_or_create(
                type=TypeChocies[attribute],
                defaults={
                'value_html': value
                }
            )
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
       'form': form,       
       'parent': 'settings',
       'segment': 'help_settings'
    }
    return render(request, 'pages/settings/help-settings.html', context)



def product_details(request, slug):
  product = get_object_or_404(Product, slug=slug)

  context = {
    'product': product,
    'related_products': Product.objects.exclude(pk=product.pk).filter(tags__in=product.tags.all())
  }
  return render(request, 'pages/product-details.html', context)


@login_required(login_url='/users/signin/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # color_id = request.POST.get('product_color')  
    # color = get_object_or_404(Color, pk=color_id)  
    # print(color,'------------------------------')

    cart, created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        is_ordered=False
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
def update_cart_quantity(request, cart_id):
   cart_item = get_object_or_404(Cart, id=cart_id)
   if request.method == 'POST':
      quantity = request.POST.get('quantity')
      cart_item.quantity = quantity
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
  demo_mode = getattr(settings, 'DEMO_MODE')
  if not demo_mode:
    if request.method == 'POST':
      StripeCredentials.objects.update_or_create(
        user=request.user,
        defaults={
          'publishable_key': request.POST.get('publishable_key'),
          'secret_key': request.POST.get('secret_key')
        }
      )
    return redirect(request.META.get('HTTP_REFERER'))
  else:
    messages.warning(request, 'DEMO Mode: Operation not allowed')
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
        order = Order.objects.create(user=request.user)
        for cart in carts:
            cart.is_ordered = True
            cart.save()       
            order.cart.add(cart)

    # Add any additional logic or redirect here
    return render(request, 'pages/payment-success.html')



@login_required(login_url='/users/signin/')
def payment_cancel(request):
   return render(request, 'pages/payment-cancel.html')



def category_page(request):
    tags = Tag.objects.filter(product__in=Product.objects.all()).distinct().annotate(
        product_count=Count('product')
    ).order_by('-product_count')

    context = {
        'tags': tags
    }
    return render(request,'pages/category-list.html', context)



def category_products(request, slug):
    tag = get_object_or_404(Tag , slug=slug)

    context = {
        'tag': tag
    }
    return render(request, 'pages/category-products.html', context)




def discounts(request):
    discounted_products = Product.objects.filter(discount__isnull=False)
    context = {
        'products': discounted_products,
    }

    return render(request, 'pages/discounted-product.html', context)


@staff_member_required
@login_required(login_url='/users/signin/')
def fetch_stripe_transactions(request):
    stripe.api_key = get_stripe_secret_key(request)
    charges = stripe.Charge.list()
    for charge in charges:
        if charge.customer:
          customer = stripe.Customer.retrieve(charge.customer)
          charge['customer_name'] = customer.name
          
        charge.amount = charge.amount / 100

    context = {
        'charges': charges
    }
    return render(request, 'pages/transaction.html', context)



@login_required(login_url='/users/signin/')
def show_order(request):
   if request.user.is_superuser:
        orders = Order.objects.all()
   else:
        orders = Order.objects.filter(user=request.user)

   
   context = {
      'orders':orders,
   }

   return render(request,'pages/order-list.html',context)





def create_props(request, product_id):
  product = Product.objects.get(pk=product_id)

  if request.method == "POST":
    props, created = ProductProps.objects.update_or_create(
      product=product,
      prop=request.POST.get('prop'),
      defaults={
        'value': request.POST.get('value')
      }
    )
  
  return redirect(request.META.get('HTTP_REFERER'))


def update_props(request, prop_id):
  product_prop = ProductProps.objects.get(pk=prop_id)

  if request.method == "POST":
    for attribute, value in request.POST.items():
      setattr(product_prop, attribute, value)
    
    product_prop.save()
  
  return redirect(request.META.get('HTTP_REFERER'))

def delete_props(request, prop_id):
  product_prop = ProductProps.objects.get(pk=prop_id)
  product_prop.delete()
  return redirect(request.META.get('HTTP_REFERER'))


def privacy_policy(request):
   legal_privacy = Settings.objects.filter(type='legal_privacy').first().value_html if Settings.objects.filter(type='legal_privacy').exists() else 'Privacy Policy'

   context = {
      'legal_privacy': legal_privacy
   }
   return render(request, 'pages/privacy-policy.html', context)

def terms_condition(request):
    legal_terms = Settings.objects.filter(type='legal_terms').first().value_html if Settings.objects.filter(type='legal_terms').exists() else 'Terms and Conditions'
    
    context = {
        'legal_terms': legal_terms
    }
    return render(request, 'pages/terms-condition.html', context)

def help(request):
    legal_help = Settings.objects.filter(type='legal_help').first().value_html if Settings.objects.filter(type='legal_help').exists() else 'Help'
    
    context = {
        'legal_help': legal_help
    }
    return render(request, 'pages/help.html', context)

@staff_member_required
@login_required(login_url='/users/signin/')
def edit_image(request, product_id, img_name):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        base64_image = request.POST.get(img_name)
        image_data = base64.b64decode(base64_image.split(',')[1])
        image_file = ContentFile(image_data, name=f'{img_name}.png')
        setattr(product, img_name, image_file)
        product.save()
        return redirect(reverse('edit_product', kwargs={'product_id': product_id}))

    context = {
       'image_path': getattr(product, img_name),
       'product': product,
       'img_name': img_name
    }
    return render(request, 'pages/edit-image.html', context)