from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("load_products/", views.load_products, name="load_products"),
    path('load-stripe-products/', views.load_stripe_products, name="load_stripe_products"),
    path('create-related-product/<int:stripe_product_id>/', views.create_related_product, name="create_related_product"),
    path('edit-product/<int:product_id>/', views.edit_product, name="edit_product"),
    path('delete-product/<int:id>/', views.delete_product, name="delete_local_product"),
    path('product/<int:product_id>/', views.product_details, name="product_details"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_list, name="cart_list"),
    path('delete-cart/<int:cart_id>/', views.delete_cart, name="delete_cart"),
    path('increment/<int:cart_id>/', views.increment_cart_item, name='cart_increment'),
    path('decrement/<int:cart_id>/', views.decrement_cart_item, name='cart_decrement'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
]
