import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField


CATEGORIES = [
    ('Movies & TV', 'Movies & TV'),
    ('Sports & Outdoors', 'Sports & Outdoors'),
    ('Fashion', 'Fashion'),
    ('Amazon Home', 'Amazon Home'),
    ('Health & Personal Care', 'Health & Personal Care'),
    ('Books', 'Books'),
    ('Toys & Games', 'Toys & Games'),
    ('Baby', 'Baby'),
    ('Office Products', 'Office Products'),
    ('All Beauty', 'All Beauty'),
    ('Arts, Crafts & Sewing', 'Arts, Crafts & Sewing'),
    ('Digital Music', 'Digital Music'),
    ('Home Audio & Theater', 'Home Audio & Theater'),
    ('Video Games', 'Video Games'),
    ('Tools & Home Improvement', 'Tools & Home Improvement'),
    ('All Electronics', 'All Electronics'),
    ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
    ('AMAZON FASHION', 'AMAZON FASHION'),
    ('Camera & Photo', 'Camera & Photo'),
    ('Industrial & Scientific', 'Industrial & Scientific'),
    ('Musical Instruments', 'Musical Instruments'),
    ('Automotive', 'Automotive'),
    ('Computers', 'Computers'),
    ('Grocery', 'Grocery'),
    ('Portable Audio & Accessories', 'Portable Audio & Accessories'),
    ('Software', 'Software'),
    ('Car Electronics', 'Car Electronics'),
    ('Pet Supplies', 'Pet Supplies'),
    ('Appliances', 'Appliances'),
    ('Collectible Coins', 'Collectible Coins'),
    ('Entertainment', 'Entertainment'),
    ('Luxury Beauty', 'Luxury Beauty'),
    ('GPS & Navigation', 'GPS & Navigation'),
    ('Amazon Devices', 'Amazon Devices')
]



class Product(models.Model):
    asin = models.CharField(auto_created=True, max_length=50, unique=True, default=uuid.uuid4)
    title = models.TextField(default="Title")
    price = models.FloatField(default=0.00)
    imageUrl = models.URLField(default="URL Here", null=True, max_length=5000)
    brand = models.TextField(default="Brand", null=True)
    description = models.TextField(default="Description", null=True)
    details = models.TextField(default="Details", null=True)
    also_view = models.CharField(max_length=900, default="Also Viewed", null=True)
    also_buy = models.CharField(max_length=1500, default="Also Bought", null=True)
    category = MultiSelectField(max_length=1500, choices=CATEGORIES, max_choices=3, default='', null=True)
    main_cat = models.CharField(max_length=28, choices=CATEGORIES, default='', null=True)
    date_added = models.DateTimeField(auto_created=True, default=timezone.now)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.title


class Review(models.Model):
    asin = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewerID = models.ForeignKey(User, on_delete=models.CASCADE)
    overall = models.IntegerField(range(0, 5))
    reviewTime = models.DateTimeField(default=timezone.now)
    reviewerName = models.TextField(null=True)
    reviewText = models.TextField(null=True)
    summary = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.reviewerID)


class Cart(models.Model):
    pass


class Checkout(models.Model):
    pass

