from atexit import register
from django.contrib import admin
from .models import PaymentMethod, Order, Item
# Register your models here.


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status', 'order_status']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']