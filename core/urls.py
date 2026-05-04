from django.contrib import admin
from django.urls import path
from .views import *
# or
# from . import views

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('product/<int:id>/', product_details, name='product_details'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove/<int:id>/', remove, name='remove'),
    path('increase/<int:id>/', qty_increase, name='qty_increase'),
    path('decrease/<int:id>/', qty_decrease, name='qty_decrease'),
    path('checkout/', checkout, name='checkout'),
    path('success/', success, name='success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order-details/<int:id>/', order_details, name='order_details'),
    path('payment/', payment, name='payment'),
    path('payment-success/', payment_success, name='payment_success'),
]