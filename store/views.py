from django.shortcuts import render, redirect
from django.db.models import Q, Avg
from store import models as store_models
from vendor import models as vendor_models

def index(request):
    products = store_models.Product.objects.filter(status='Published')

    context = {
        'products': products,
        'new_products': store_models.Product.objects.filter(status='Published', featured=True).order_by('-date')[:4],
    }

    return render(request, 'store/index.html', context)


def products(request):
    products = store_models.Product.objects.filter(status='Published').select_related('vendor')
    vendors = vendor_models.Vendor.objects.all()

    context = {
        'products': products,
        'vendors': vendors
    }

    return render(request, 'store/products.html', context)


def product_detail(request, slug):
    product = store_models.Product.objects.get(status='Published', slug=slug)
    related_products = store_models.Product.objects.filter(category=product.category, status='Published').exclude(id=product.id)
    # variant_items = []
    # for variant in product.variants():
    #     for item in variant.variant_items.all():
    #         if item.title == 'Weight' or item.title == 'weight' or item.title =='Size' or item.title == 'size':
    #             item.description_list = item.description.split(',')
    #             variant_items.append(item)

    context = {
        'product': product,
        'related_products': related_products,
        # 'variant_items': variant_items,
    }

    return render(request, 'store/product-detail.html', context)


def categories(request):
    categories = store_models.Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'store/categories.html', context)


def category_products(request, slug):
    category = store_models.Category.objects.get(slug=slug)
    products = store_models.Product.objects.filter(status='Published', category=category)

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'store/category-products.html', context)


def vendors(request):
    vendors = vendor_models.Vendor.objects.all()

    context = {
        'vendors': vendors
    }

    return render(request, 'store/vendors.html', context)


def vendor_detail(request, slug):
    vendor = vendor_models.Vendor.objects.get(slug=slug)

    context = {
        'vendor': vendor
    }

    return render(request, 'store/vendor-detail.html', context)


