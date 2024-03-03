from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("starter/", views.starter, name="starter"),

    path('load-stripe-products/', views.load_stripe_products, name="load_stripe_products")
]
