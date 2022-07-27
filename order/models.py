from itertools import product
from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product


class PaymentMethod(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


# Create your models here.
class Order(models.Model):
    order_status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    ]
    payment_status_choices = [
        ('Not Paid', 'Not Paid'),
        ('Success', 'Success'),
        ('Canceled', 'Canceled'),
        ('Failed', 'Failed'),
    ]
    user = models.ForeignKey(get_user_model(), models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, through='Item', blank=True)
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='Not Paid', null=True, blank=True)
    transaction_id = models.CharField(unique=True ,max_length=250, blank=True, null=True)
    paid_amount = models.DecimalField(decimal_places=2, max_digits=15, default=0, blank=True, null=True)
    bill_amount = models.DecimalField(decimal_places=2, max_digits=15, default=0, blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=order_status_choices, default='Pending', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}"

    def save(self, *args, **kwargs):
        if self.payment_status == 'Success':
            items = Item.objects.filter(order__id=self.pk)
            for item in items:
                if item.product.stock_amount > item.quantity:
                    item.product.stock_amount = item.product.stock_amount - item.quantity
                    item.product.save()
        super(Order, self).save(*args, **kwargs)


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True)
    product = models.ForeignKey(Product,related_name='Items', on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.order}, {self.product}, {self.quantity}"

