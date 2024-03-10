from django.urls import path

from . import views

urlpatterns = [
    path("", views.datatables, name="datatables"),
    path('delete-product/<int:id>/', views.delete_product, name="delete_product"),
    path('update-product/<int:id>/', views.update_product, name="update_product"),
    path('increment/<int:cart_id>/', views.increment_cart_item, name='cart_increment'),
    path('decrement/<int:cart_id>/', views.decrement_cart_item, name='cart_decrement'),
]