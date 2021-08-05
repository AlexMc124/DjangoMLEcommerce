# Generated by Django 3.0.7 on 2021-04-16 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_auto_20210415_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewerID', models.CharField(auto_created=True, editable=False, max_length=20, null=True, unique=True)),
                ('profile_image', models.ImageField(default='defaultpictures/default.jpg', upload_to='profile_pics')),
                ('interests', models.CharField(choices=[('Movies & TV', 'Movies & TV'), ('Sports & Outdoors', 'Sports & Outdoors'), ('Fashion', 'Fashion'), ('Amazon Home', 'Amazon Home'), ('Health & Personal Care', 'Health & Personal Care'), ('Books', 'Books'), ('Toys & Games', 'Toys & Games'), ('Baby', 'Baby'), ('Office Products', 'Office Products'), ('All Beauty', 'All Beauty'), ('Arts, Crafts & Sewing', 'Arts, Crafts & Sewing'), ('Digital Music', 'Digital Music'), ('Home Audio & Theater', 'Home Audio & Theater'), ('Video Games', 'Video Games'), ('Tools & Home Improvement', 'Tools & Home Improvement'), ('All Electronics', 'All Electronics'), ('Cell Phones & Accessories', 'Cell Phones & Accessories'), ('AMAZON FASHION', 'AMAZON FASHION'), ('Camera & Photo', 'Camera & Photo'), ('Industrial & Scientific', 'Industrial & Scientific'), ('Musical Instruments', 'Musical Instruments'), ('Automotive', 'Automotive'), ('Computers', 'Computers'), ('Grocery', 'Grocery'), ('Portable Audio & Accessories', 'Portable Audio & Accessories'), ('Software', 'Software'), ('Car Electronics', 'Car Electronics'), ('Pet Supplies', 'Pet Supplies'), ('Appliances', 'Appliances'), ('Collectible Coins', 'Collectible Coins'), ('Entertainment', 'Entertainment'), ('Luxury Beauty', 'Luxury Beauty'), ('GPS & Navigation', 'GPS & Navigation'), ('Amazon Devices', 'Amazon Devices')], default='', max_length=28, null=True)),
                ('cart', models.ManyToManyField(blank=True, to='store.Product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
