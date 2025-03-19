from django.shortcuts import render, redirect
from vendor import models as vendor_models
from store import models as store_models


def vendor_list(request):
    vendors = vendor_models.Vendor.objects.all()

    for vendor in vendors:
        vendor.avg_rating = round(vendor.average_rating(), 1)
        vendor.total_reviews = vendor.review_count()
        vendor.products = store_models.Product.objects.filter(vendor=vendor.user, status='Published').order_by('-date')[:5]
        vendor.total_products = store_models.Product.objects.filter(vendor=vendor.user, status='Published').count()

    context = {
        'vendors': vendors
    }

    return render(request, 'vendor/vendors.html', context)