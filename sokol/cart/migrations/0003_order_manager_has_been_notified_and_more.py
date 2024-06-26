# Generated by Django 5.0.2 on 2024-03-28 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_order_telegram_order_order_vk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='manager_has_been_notified',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Менеджер уведомлен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Номер заказа'),
        ),
    ]
