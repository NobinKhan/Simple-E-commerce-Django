import imp
from django.contrib import admin
from .models import Cart, Item
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')


@admin.register(Item)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')