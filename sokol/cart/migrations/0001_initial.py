# Generated by Django 5.0.2 on 2024-03-26 22:36

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')),
                ('ordered_products', models.TextField(verbose_name='Список заказанных товаров')),
                ('order_price', models.FloatField(verbose_name='Стоимость заказа в рублях')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')),
                ('order_status', models.CharField(choices=[('awaiting_payment', 'Ожидает оплаты'), ('in_assembly', 'В сборке'), ('transferred_to_delivery', 'Передаётся в доставку'), ('on_the_way', 'В пути'), ('awaiting_receipt', 'Ожидает получения'), ('received', 'Получен '), ('canceled', 'Отменен')], default='awaiting_payment', max_length=40, verbose_name='Статус заказа')),
                ('customer_last_name', models.CharField(max_length=150, verbose_name='Фамилия заказчика')),
                ('customer_first_name', models.CharField(max_length=150, verbose_name='Имя заказчика')),
                ('customer_patronymic', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество заказчика')),
                ('order_email', models.EmailField(max_length=254, verbose_name='Почта заказчика')),
                ('order_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Тлефон заказчика')),
                ('order_delivery_method', models.CharField(max_length=150, verbose_name='Выбранный способ доставки')),
                ('order_region', models.CharField(max_length=150, verbose_name='Область')),
                ('order_city', models.CharField(max_length=150, verbose_name='Населенный пункт')),
                ('order_street', models.CharField(blank=True, max_length=150, null=True, verbose_name='Улица')),
                ('order_house', models.CharField(blank=True, max_length=150, null=True, verbose_name='Дом')),
                ('order_flat', models.CharField(blank=True, max_length=150, null=True, verbose_name='Квартира')),
                ('order_entrance', models.CharField(blank=True, max_length=150, null=True, verbose_name='Подъезд')),
                ('order_floor', models.CharField(blank=True, max_length=150, null=True, verbose_name='Этаж')),
                ('order_intercom', models.CharField(blank=True, max_length=150, null=True, verbose_name='Домофон')),
                ('order_comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
