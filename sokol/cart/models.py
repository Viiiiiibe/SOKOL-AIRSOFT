from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()


class Order(models.Model):
    STATUS_OPTIONS = (
        ('awaiting_payment', 'Ожидает оплаты'),
        ('in_assembly', 'В сборке'),
        ('transferred_to_delivery', 'Передаётся в доставку'),
        ('on_the_way', 'В пути'),
        ('awaiting_receipt', 'Ожидает получения'),
        ('received', 'Получен '),
        ('canceled', 'Отменен')
    )
    order_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name='Номер заказа')
    # ordered_products = models.TextField()
    ordered_products = models.TextField(verbose_name='Список заказанных товаров', )
    # ordered_products = models.ManyToManyField(
    #     Product,
    #     related_name='orders',
    #     verbose_name='Список заказанных товаров'
    # )
    order_price = models.FloatField(verbose_name='Стоимость заказа в рублях')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    # оплачен, в сборке, отправлено, получен
    order_status = models.CharField(choices=STATUS_OPTIONS, default='awaiting_payment', verbose_name='Статус заказа',
                                    max_length=40)
    # если заказал авторизованный
    customer = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='Заказчик'
    )
    customer_last_name = models.CharField(max_length=150, verbose_name='Фамилия заказчика')
    customer_first_name = models.CharField(max_length=150, verbose_name='Имя заказчика')
    customer_patronymic = models.CharField(blank=True, null=True, max_length=150, verbose_name='Отчество заказчика')
    order_email = models.EmailField(verbose_name='Почта заказчика')
    order_phone = PhoneNumberField(blank=False, null=True, verbose_name='Тлефон заказчика')
    order_vk = models.CharField(blank=True, null=True, max_length=150, verbose_name='VK заказчика')
    order_telegram = models.CharField(blank=True, null=True, max_length=150, verbose_name='Telegram заказчика')
    order_delivery_method = models.CharField(max_length=150, verbose_name='Выбранный способ доставки')
    # order_address = models.TextField(verbose_name='Адрес доставки')
    order_region = models.CharField(max_length=150, verbose_name='Область')
    order_city = models.CharField(max_length=150, verbose_name='Населенный пункт')
    order_street = models.CharField(blank=True, null=True, max_length=150, verbose_name='Улица')
    order_house = models.CharField(blank=True, null=True, max_length=150, verbose_name='Дом')
    order_flat = models.CharField(blank=True, null=True, max_length=150, verbose_name='Квартира')
    order_entrance = models.CharField(blank=True, null=True, max_length=150, verbose_name='Подъезд')
    order_floor = models.CharField(blank=True, null=True, max_length=150, verbose_name='Этаж')
    order_intercom = models.CharField(blank=True, null=True, max_length=150, verbose_name='Домофон')
    order_comment = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True, )
    manager_has_been_notified = models.BooleanField(verbose_name='Менеджер уведомлен', blank=True, null=True,
                                                    default=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"{1000 + Order.objects.all().count() + 1}"
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ из магазина'
        verbose_name_plural = 'Заказы из магазина'


class DeliveryOrder(models.Model):
    STATUS_OPTIONS = (
        ('awaiting_payment', 'Ожидает оплаты'),
        ('in_assembly', 'В сборке'),
        ('transferred_to_delivery', 'Передаётся в доставку'),
        ('on_the_way', 'В пути'),
        ('awaiting_receipt', 'Ожидает получения'),
        ('received', 'Получен '),
        ('canceled', 'Отменен')
    )
    order_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name='Номер заказа')
    order_description = models.TextField(verbose_name='Описание', )
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    order_status = models.CharField(choices=STATUS_OPTIONS, default='awaiting_payment', verbose_name='Статус заказа',
                                    max_length=40)
    customer = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='delivery_orders',
        verbose_name='Заказчик'
    )
    customer_last_name = models.CharField(max_length=150, verbose_name='Фамилия заказчика')
    customer_first_name = models.CharField(max_length=150, verbose_name='Имя заказчика')
    customer_patronymic = models.CharField(blank=True, null=True, max_length=150, verbose_name='Отчество заказчика')
    order_email = models.EmailField(verbose_name='Почта заказчика')
    order_phone = PhoneNumberField(blank=False, null=True, verbose_name='Тлефон заказчика')
    order_vk = models.CharField(blank=True, null=True, max_length=150, verbose_name='VK заказчика')
    order_telegram = models.CharField(blank=True, null=True, max_length=150, verbose_name='Telegram заказчика')
    order_delivery_method = models.CharField(max_length=150, verbose_name='Выбранный способ доставки')
    order_region = models.CharField(max_length=150, verbose_name='Область')
    order_city = models.CharField(max_length=150, verbose_name='Населенный пункт')
    order_street = models.CharField(blank=True, null=True, max_length=150, verbose_name='Улица')
    order_house = models.CharField(blank=True, null=True, max_length=150, verbose_name='Дом')
    order_flat = models.CharField(blank=True, null=True, max_length=150, verbose_name='Квартира')
    order_entrance = models.CharField(blank=True, null=True, max_length=150, verbose_name='Подъезд')
    order_floor = models.CharField(blank=True, null=True, max_length=150, verbose_name='Этаж')
    order_intercom = models.CharField(blank=True, null=True, max_length=150, verbose_name='Домофон')
    order_comment = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True, )
    manager_has_been_notified = models.BooleanField(verbose_name='Менеджер уведомлен', blank=True, null=True,
                                                    default=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"{1000 + DeliveryOrder.objects.all().count() + 1}"
        super(DeliveryOrder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ на доставку'
        verbose_name_plural = 'Заказы на доставку'
