# Generated by Django 3.0.7 on 2021-04-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210415_2238'),
        ('users', '0004_remove_profile_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cart',
            field=models.ManyToManyField(blank=True, to='store.Product'),
        ),
    ]
