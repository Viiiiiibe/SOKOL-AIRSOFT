# Generated by Django 5.0.2 on 2024-03-23 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_order_order_number_alter_product_image1_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]