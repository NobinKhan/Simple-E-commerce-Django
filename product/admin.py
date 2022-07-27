from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'new_price', 'stock_amount', 'status')
    prepopulated_fields = {'slug': ('name',)}