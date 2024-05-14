# Generated by Django 5.0.2 on 2024-03-02 22:44

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название в URL')),
                ('image', models.ImageField(default='/сategory_img/default_сategory_img.jpg', upload_to='сategory_img/', verbose_name='Картинка 896x485 для показа в списках')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.TextField(verbose_name='Название')),
                ('product_description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие')),
                ('items_left', models.IntegerField(blank=True, null=True, verbose_name='Осталось единиц товара')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('image1', models.ImageField(blank=True, upload_to='product_img/', verbose_name='Картинка 536x639 для страницы продукта')),
                ('image2', models.ImageField(blank=True, upload_to='product_img/', verbose_name='Картинка 536x639 для страницы продукта')),
                ('image3', models.ImageField(blank=True, upload_to='product_img/', verbose_name='Картинка 536x639 для страницы продукта')),
                ('image4', models.ImageField(blank=True, upload_to='product_img/', verbose_name='Картинка 536x639 для страницы продукта')),
                ('image5', models.ImageField(blank=True, upload_to='product_img/', verbose_name='Картинка 1140x760 для страницы продукта')),
                ('image6', models.ImageField(default='/product_img/default_product_img.jpg', upload_to='product_img/', verbose_name='Картинка 433x516 для показа в списках')),
                ('link_to_a_video', models.TextField(blank=True, verbose_name='Ссылка на видео')),
                ('recommend', models.BooleanField(default=False, verbose_name='Рекомендовать')),
                ('product_type', models.TextField(blank=True, null=True, verbose_name='Тип товара')),
                ('compatibility', models.TextField(blank=True, null=True, verbose_name='Совместимость')),
                ('thread_type', models.TextField(blank=True, null=True, verbose_name='Тип резьбы')),
                ('mounting_type', models.TextField(blank=True, null=True, verbose_name='Тип крепления')),
                ('imitation_of_a_shot', models.BooleanField(blank=True, null=True, verbose_name='Имитация выстрела')),
                ('laser_sight', models.BooleanField(blank=True, null=True, verbose_name='С ЛЦУ:')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='Вес в гр.')),
                ('principle_of_operation', models.TextField(blank=True, null=True, verbose_name='Принцип действия')),
                ('length', models.IntegerField(blank=True, null=True, verbose_name='Длина в мм')),
                ('diameter', models.FloatField(blank=True, null=True, verbose_name='Диаметр в мм')),
                ('girbox', models.TextField(blank=True, null=True, verbose_name='Гирбокс')),
                ('category', models.ManyToManyField(related_name='products', to='products.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_price', models.FloatField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_delivery_method', models.TextField()),
                ('ordered_address', models.TextField()),
                ('ordered_status', models.TextField()),
                ('order_email', models.EmailField(max_length=254)),
                ('order_phone', models.CharField(blank=True, max_length=12, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('ordered_products', models.ManyToManyField(related_name='orders', to='products.product')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]