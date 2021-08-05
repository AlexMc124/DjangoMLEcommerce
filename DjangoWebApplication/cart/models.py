from django.db import models
from django.db.models import Sum

from users.models import Profile
from store.models import Product


class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.title


class Order(models.Model):
    ref_code = models.CharField(max_length=20)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        x = Product.objects.filter(pk__in=self.items.all()).aggregate(Sum('price'))
        return list(x.values())[0]


    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)
