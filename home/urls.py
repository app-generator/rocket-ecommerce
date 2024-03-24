from django.urls import path

from . import views

urlpatterns = [
    path("admin-ui", views.dashboard, name="index"),
    path("load_products/", views.load_products, name="load_products"),
    path('load-stripe-products/', views.load_stripe_products, name="load_stripe_products"),
    path('create-related-product/<int:stripe_product_id>/', views.create_related_product, name="create_related_product"),
    path('edit-product/<int:product_id>/', views.edit_product, name="edit_product"),
    path('edit-image/<int:product_id>/<str:img_name>/', views.edit_image, name="edit_image"),
    path('delete-product/<int:id>/', views.delete_local_product, name="delete_local_product"),
    path('delete-product/<int:local_product>/<int:stripe_product>/', views.delete_both_product, name="delete_both_product"),
    path('product/<str:slug>/', views.product_details, name="product_details"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),

    #Cart
    path('cart/', views.cart_list, name="cart_list"),
    path('delete-cart/<int:cart_id>/', views.delete_cart, name="delete_cart"),
    path('increment/<int:cart_id>/', views.increment_cart_item, name='cart_increment'),
    path('decrement/<int:cart_id>/', views.decrement_cart_item, name='cart_decrement'),
    path('update-cart-quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    #Stripe
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe-credentials/', views.add_stripe_credentials, name='add_stripe_credentials'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),

    #Category
    path('category-list/', views.category_page, name='category_list'),
    path('category-product/<str:slug>/', views.category_products, name='category_products'),

    #Discount
    path('discounts/', views.discounts, name='discounts'),

    #homepage
    path('', views.homepage, name='home_page'),
    path('tag/<str:slug>/', views.homepage, name='home_page'),
    path('transaction/', views.fetch_stripe_transactions, name='transaction'),

    #Order
    path('order-list/',views.show_order, name = 'order_list'),

    path('search/', views.search_page, name="search_page"),

    path('create-props/<int:product_id>/', views.create_props, name="create_props"),
    path('update-props/<int:prop_id>/', views.update_props, name="update_props"),
    path('delete-props/<int:prop_id>/', views.delete_props, name="delete_props"),

    # settings
    path('settings/stripe/', views.stripe_settings, name="stripe_settings"),
    path('settings/general/', views.general_settings, name="general_settings"),
    path('settings/social/', views.social_settings, name="social_settings"),
    path('settings/privacy-policy/', views.privacy_settings, name="privacy_settings"),
    path('settings/terms-condition/', views.terms_settings, name="terms_settings"),
    path('settings/help/', views.help_settings, name="help_settings"),

    # legal
    path('privacy/', views.privacy_policy, name="privacy_policy"),
    path('terms/', views.terms_condition, name="terms_condition"),
    path('help/', views.help, name="help"),

]
