# Generated by Django 3.0.7 on 2021-04-16 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_weed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='weed',
        ),
    ]
