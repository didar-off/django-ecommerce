# Generated by Django 4.2 on 2024-10-29 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/images')),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('discount', models.IntegerField(default=1)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=10, prefix='')),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('service_fee', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Processing', 'Processing'), ('Failed', 'Failed')], default='Processing', max_length=100)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('PayPal', 'PayPal'), ('Stripe', 'Stripe'), ('Flutterwave', 'Flutterwave'), ('Paystack', 'Paystack'), ('RazorPay', 'RazorPay')], default='Cash', max_length=100)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('initial_total', models.DecimalField(decimal_places=2, help_text='The original total before discounts', max_digits=10)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount saved with coupon', max_digits=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('coupons', models.ManyToManyField(to='store.coupon')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='default-product.jpg', upload_to='product/images')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description')),
                ('short_inf', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Short Information')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Sale Price')),
                ('regular_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Regular Price')),
                ('stock', models.PositiveIntegerField(blank=True, default=10, null=True)),
                ('shipping', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Shipping Amount')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Disabled', 'Disabled')], default='Draft', max_length=50)),
                ('featured', models.BooleanField(default=False, verbose_name='Marketplace Featured')),
                ('type', models.CharField(default='Organic', max_length=100)),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=10, prefix='SKU', unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('life', models.PositiveSmallIntegerField(default=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Variant Name')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Variant Item Title')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Variant Item Description')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_items', to='store.variant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=10, prefix='')),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('shipping_service', models.CharField(choices=[('DHL', 'DHL'), ('FedX', 'FedX'), ('UPS', 'UPS'), ('GIG Logistics', 'GIG Logistics')], default=None, max_length=100)),
                ('tracking_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('qty', models.PositiveSmallIntegerField(default=0)),
                ('weight', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('initial_total', models.DecimalField(decimal_places=2, help_text='Grand Total of all amount', max_digits=10)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Saved Amount', max_digits=10, null=True)),
                ('applied_coupon', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('coupon', models.ManyToManyField(to='store.coupon')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_order_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery/images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(max_length=100)),
                ('qty', models.PositiveSmallIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]