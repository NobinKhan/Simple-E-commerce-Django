from django.db import models
from decimal   import Decimal
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/product/')
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0,validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    stock_amount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    min_order_amount = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
