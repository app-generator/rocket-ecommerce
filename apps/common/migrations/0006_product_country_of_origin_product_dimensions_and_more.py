# Generated by Django 4.2.9 on 2024-03-18 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_remove_order_cart_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='country_of_origin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='dimensions',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]