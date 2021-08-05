from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import *

from cart.extras import generate_order_id
from cart.models import OrderItem, Order
from store.models import Product
from users.models import Profile


def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    print(user_profile.id)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('pk', "")).first()
    print(product)
    # check if the user already owns this product
    if product in request.user.profile.cart.all():
        messages.info(request, 'You already own this Product')
        return redirect(reverse('store-home'))
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "Product added to Cart")
    return redirect(reverse('store-home'))


@login_required()
def delete_from_cart(request, pk):
    item_to_delete = OrderItem.objects.filter(pk=pk)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Product has been deleted")
    return redirect(reverse('store-home'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
                'order': existing_order,
    }
    return render(request, 'cart/order_summary.html', context)


@login_required()
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
    }
    return render(request, 'cart/checkout.html', context)



