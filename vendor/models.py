from django.db import models
from django.db.models import Avg, Count
import uuid
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from userauths.models import User
from django.utils.text import slugify

from store import models as store_models


NOTIFICATION_TYPE = (
    ('New Order', 'New Order'),
    ('New Review', 'New Review'),
)


PAYOUT_METHOD = (
    ('Cash', 'Cash'),
    ('PayPal', 'PayPal'),
    ('Stripe', 'Stripe'),
    ('Flutterwave', 'Flutterwave'),
    ('Paystack', 'Paystack'),
    ('RazorPay', 'RazorPay'),
)


TYPE = (
    ('New Order', 'New Order'),
    ('Item Shipped', 'Item Shipped'),
    ('Item Delivered', 'Item Delivered'),
)


class Vendor(models.Model):
    store_name = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')

    image = models.ImageField(upload_to='vendor/images', default='default-vendor.png', blank=True)
    description = CKEditor5Field('Description', config_name='extends')
    country = models.CharField(max_length=100, null=True, blank=True)

    vendor_id = ShortUUIDField(unique=True, max_length=10, length=5, alphabet='1234567890')
    
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.store_name
    
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.store_name)
        super(Vendor, self).save(*args, **kwargs)

    def average_rating(self):
        avg = store_models.Product.objects.filter(vendor=self.user, reviews__active=True).aggregate(avg_rating=Avg('reviews__rating'))['avg_rating']
        return avg if avg is not None else 0
    
    def review_count(self):
        rw_count = store_models.Product.objects.filter(vendor=self.user, reviews__active=True).aggregate(review_count=Count('reviews'))['review_count']
        return rw_count if rw_count is not None else 0


class Payout(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey('store.OrderItem', on_delete=models.SET_NULL, null=True, blank=True, related_name='payout')

    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, null=True, blank=True)
    payout_id = ShortUUIDField(unique=True, max_length=10, length=5, alphabet='1234567890')

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payout'
        verbose_name_plural = 'Payouts'
        ordering = ['-date']

    def __str__(self):
        return self.vendor
    

class BankAccount(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.SET_NULL, null=True)
    account_type = models.CharField(max_length=50, choices=PAYOUT_METHOD, null=True, blank=True)

    bank_name = models.CharField(max_length=250)
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=100, null=True, blank=True)

    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    paypal_address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'BankAccount'
        verbose_name_plural = 'BankAccounts'

    def __str__(self):
        return self.bank_name
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_notification', null=True)

    type = models.CharField(max_length=100, choices=TYPE, default=None)
    order = models.ForeignKey('store.OrderItem', on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return self.type

