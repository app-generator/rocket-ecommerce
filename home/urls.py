from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("starter/", views.starter, name="starter"),

    path('load-stripe-products/', views.load_stripe_products, name="load_stripe_products"),
    path('create-related-product/<int:stripe_product_id>/', views.create_related_product, name="create_related_product"),
    path('edit-product/<int:product_id>/', views.edit_product, name="edit_product"),
]
