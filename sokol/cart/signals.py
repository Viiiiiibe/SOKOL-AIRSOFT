from smtplib import SMTPDataError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, DeliveryOrder
from sokol.settings import EMAIL_HOST_USER, MANAGER_EMAIL
from django.core.mail import send_mail
from django.template.loader import get_template
import logging

logger = logging.getLogger('django')


@receiver(post_save, sender=Order)
def send_email_to_manager_with_order(instance, **kwargs):
    context = {
        'order': instance
    }
    if not instance.manager_has_been_notified:
        try:
            send_mail(
                "Заявка на заказ из магазина",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{MANAGER_EMAIL}"],
                fail_silently=False,
                html_message=get_template('email/order_confirm_to_manager.html').render(context)
            )
            Order.objects.filter(pk=instance.pk).update(manager_has_been_notified=True)
        except SMTPDataError:
            logger.info(f"SMTPDataError, email to manager with order {instance.order_number} not sent")


@receiver(post_save, sender=DeliveryOrder)
def send_email_to_manager_with_delivery_order(instance, **kwargs):
    context = {
        'order': instance
    }
    if not instance.manager_has_been_notified:
        try:
            send_mail(
                "Заявка на доставку",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{MANAGER_EMAIL}"],
                fail_silently=False,
                html_message=get_template('email/delivery_order_confirm_to_manager.html').render(context)
            )
            DeliveryOrder.objects.filter(pk=instance.pk).update(manager_has_been_notified=True)
        except SMTPDataError:
            logger.info(f"SMTPDataError, email to manager with delivery order {instance.order_number} not sent")


@receiver(post_save, sender=Order)
def send_email_to_customer_with_order(instance, **kwargs):
    context = {
        'order': instance
    }
    if not instance.manager_has_been_notified:
        try:
            send_mail(
                "Заказ оформлен",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{instance.order_email}"],
                fail_silently=False,
                html_message=get_template('email/order_confirm_to_customer.html').render(context)
            )
        except SMTPDataError:
            logger.info(f"SMTPDataError, email to customer with order {instance.order_number} confirmation not sent")


@receiver(post_save, sender=DeliveryOrder)
def send_email_to_customer_with_delivery_order(instance, **kwargs):
    context = {
        'order': instance
    }
    if not instance.manager_has_been_notified:
        try:
            send_mail(
                "Заявка оформлена",
                '',
                f"{EMAIL_HOST_USER}",
                [f"{instance.order_email}"],
                fail_silently=False,
                html_message=get_template('email/delivery_order_confirm_to_customer.html').render(context)
            )
        except SMTPDataError:
            logger.info(
                f"SMTPDataError, email to customer with delivery order {instance.order_number} confirmation not sent")
