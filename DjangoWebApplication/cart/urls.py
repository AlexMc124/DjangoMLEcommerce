from django.conf.urls import url
from django.urls import path

from .views import *


urlpatterns = [
    path('add-to-cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('order-summary/', order_details, name='order_summary'),
    path('item/delete/<pk>/', delete_from_cart, name='delete_from_cart'),
    path('checkout/', checkout, name='checkout'),
]