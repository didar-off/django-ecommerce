from django.shortcuts import render, redirect
from store import models as store_models


def index(request):
    products = store_models.Product.objects.filter(status='Published')

    context = {
        'products': products
    }

    return render(request, 'store/index.html', context)


def product_detail(request, slug):
    product = store_models.Product.objects.get(status='Published', slug=slug)
    related_products = store_models.Product.objects.filter(category=product.category, status='Published').exclude(id=product.id)

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'store/product-detail.html', context)