from django.contrib import admin
from .models import Order, DeliveryOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order_number', 'order_date', 'order_price', 'order_email', 'manager_has_been_notified',
                    'order_status')
    search_fields = ('pk', 'order_number', 'order_email',)
    list_filter = ('manager_has_been_notified', 'order_status')
    list_editable = ('order_status',)


class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order_number', 'order_date', 'order_email', 'manager_has_been_notified', 'order_status')
    search_fields = ('pk', 'order_number', 'order_email',)
    list_filter = ('manager_has_been_notified', 'order_status')
    list_editable = ('order_status',)


admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryOrder, DeliveryOrderAdmin)
