# Generated by Django 5.0.2 on 2024-03-28 19:06

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_telegram',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Telegram заказчика'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_vk',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='VK заказчика'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Тлефон заказчика'),
        ),
    ]
