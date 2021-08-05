from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Product, Review

@receiver(post_save, sender=Product)
def newproductupdatemodel(sender, instance, created, **kwargs):
    pass


@receiver(post_save, sender=Review)
def newreviewupdatemodel(sender, instance, created, **kwargs):
    pass

