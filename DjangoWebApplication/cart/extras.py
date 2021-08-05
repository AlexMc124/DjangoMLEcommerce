import random
import string
import datetime
from datetime import date

from .models import OrderItem


def saveOrderItem(order):
    order_item = OrderItem.objects.get_or_create(order=order)
    order_item.save()
    return order_item


def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now())
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str