# Generated by Django 4.0.6 on 2022-07-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_stock_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='min_order_amount',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]