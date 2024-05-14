from django import forms
from .models import Order, DeliveryOrder
from phonenumber_field.formfields import PhoneNumberField


class MakingAnOrderForm(forms.ModelForm):
    customer_last_name = forms.CharField
    customer_first_name = forms.CharField
    customer_patronymic = forms.CharField
    order_email = forms.EmailField
    order_phone = PhoneNumberField
    order_vk = forms.CharField
    order_telegram = forms.CharField

    class Meta:
        model = Order
        # fields = "__all__"
        fields = ('customer_last_name', 'customer_first_name', 'customer_patronymic', 'order_email', 'order_phone',
                  'order_vk', 'order_telegram', 'order_comment',)


class MakingAnDeliveryOrderForm(forms.ModelForm):
    customer_last_name = forms.CharField
    customer_first_name = forms.CharField
    customer_patronymic = forms.CharField
    order_email = forms.EmailField
    order_phone = PhoneNumberField
    order_vk = forms.CharField
    order_telegram = forms.CharField

    class Meta:
        model = DeliveryOrder
        # fields = "__all__"
        fields = ('customer_last_name', 'customer_first_name', 'customer_patronymic', 'order_email', 'order_phone',
                  'order_vk', 'order_telegram', 'order_comment',)
