from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, through='Item', blank=True)
    # total_amount = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def get_total_price(self):
        pr = self.product.all()
        total = 0
        for prt in pr:
            item = Item.objects.get(cart__id=self.id, product=prt)
            total = total + item.get_price()
        return total
            

    def __str__(self):
        return str(self.user)


class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, default=1)
    # price = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # conditions=Q(is_active=True),
                fields=["cart", "product"],
                name="unique_cart"
            )
        ]

    def get_price(self):
        return self.quantity * self.product.new_price

    def __str__(self):
        return f"{self.cart} {self.product} {self.quantity}"