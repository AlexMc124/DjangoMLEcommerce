from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from store.models import Product

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='defaultpictures/default.jpg', upload_to='profile_pics')
    INTEREST_CHOICES = [
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
    interests = models.CharField(max_length=28, choices=INTEREST_CHOICES, default='', null=True)
    cart = models.ManyToManyField(Product, blank=True)


    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
