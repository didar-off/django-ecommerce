# Generated by Django 4.2 on 2024-10-31 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_cart_weight_remove_orderitem_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='life',
            field=models.CharField(default='10 days', max_length=100),
        ),
    ]