from django.test import TestCase
from ..models import Order, DeliveryOrder
from django.core import mail
from sokol.settings import DEFAULT_FROM_EMAIL, MANAGER_EMAIL


class SendEmails(TestCase):
    def test_send_emails_with_order(self):
        Order.objects.create(
            order_price=100000,
            order_email='name@gmail.com',

        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Заявка на заказ из магазина')
        self.assertEqual(mail.outbox[0].body, '')
        self.assertEqual(mail.outbox[0].from_email, f"{DEFAULT_FROM_EMAIL}")
        self.assertEqual(mail.outbox[0].to, [f'{MANAGER_EMAIL}'])

        self.assertEqual(mail.outbox[1].subject, 'Заказ оформлен')
        self.assertEqual(mail.outbox[1].body, '')
        self.assertEqual(mail.outbox[1].from_email, f"{DEFAULT_FROM_EMAIL}")
        self.assertEqual(mail.outbox[1].to, ['name@gmail.com'])

    def test_send_emails_with_delivery_order(self):
        DeliveryOrder.objects.create(
            order_email='name@gmail.com',
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Заявка на доставку')
        self.assertEqual(mail.outbox[0].body, '')
        self.assertEqual(mail.outbox[0].from_email, f"{DEFAULT_FROM_EMAIL}")
        self.assertEqual(mail.outbox[0].to, [f'{MANAGER_EMAIL}'])

        self.assertEqual(mail.outbox[1].subject, 'Заявка оформлена')
        self.assertEqual(mail.outbox[1].body, '')
        self.assertEqual(mail.outbox[1].from_email, f"{DEFAULT_FROM_EMAIL}")
        self.assertEqual(mail.outbox[1].to, ['name@gmail.com'])
