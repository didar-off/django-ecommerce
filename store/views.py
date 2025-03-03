from django.shortcuts import render, redirect
from django.http import JsonResponse
from store import models as store_models
from decimal import Decimal
from django.db.models import Q, Avg, Sum


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


def products(request):
    products = store_models.Product.objects.filter(status='Published')

    context = {
        'products': products
    }

    return render(request, 'store/products.html', context)


def add_to_cart(request):
    id = request.GET.get('id')
    qty = request.GET.get('qty')
    weight = request.GET.get('weight')
    color = request.GET.get('color')
    cart_id = request.GET.get('cart_id')

    request.session['cart_id'] = cart_id

    if not id or not qty or not cart_id:
        return JsonResponse({'error': 'No id, qty or cart_id'}, status=400)
    
    try:
        product = store_models.Product.objects.get(status='Published', id=id)
    except store_models.Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=400)
    
    existing_cart_items = store_models.Cart.objects.filter(cart_id=cart_id, product=product).first()
    if int(qty) > product.stock:
        return JsonResponse({'error': 'Qty exceed current stock amount'}, status=404)
    
    if not existing_cart_items:
        cart = store_models.Cart()
        cart.product = product
        cart.qty = qty
        cart.price = product.price
        cart.weight = weight
        cart.color = color
        cart.sub_total = Decimal(product.price) * Decimal(qty)
        cart.shipping = Decimal(product.shipping)
        cart.total = cart.sub_total + cart.shipping
        cart.user = request.user if request.user.is_authenticated else None
        cart.cart_id = cart_id
        cart.save()

        message = 'Item added to cart'
    else:
        existing_cart_items.product = product
        existing_cart_items.qty = qty
        existing_cart_items.price = product.price
        existing_cart_items.weight = weight
        existing_cart_items.color = color
        existing_cart_items.sub_total = Decimal(product.price) * Decimal(qty)
        existing_cart_items.shipping = Decimal(product.shipping)
        existing_cart_items.total = existing_cart_items.sub_total + existing_cart_items.shipping
        existing_cart_items.user = request.user if request.user.is_authenticated else None
        existing_cart_items.cart_id = cart_id
        existing_cart_items.save()

        message = 'Cart Updated'

    total_cart_items = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(cart_id=cart_id))
    cart_sub_total = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(cart_id=cart_id)).aggregate(sub_total=Sum('sub_total'))['sub_total']

    return JsonResponse({
        'message': message,
        'total_cart_items': total_cart_items.count(),
        'cart_sub_total': '{:,.2f}'.format(cart_sub_total),
        'item_sub_total': '{:,.2f}'.format(existing_cart_items.sub_total) if existing_cart_items else '{:,.2f}'.format(cart.sub_total),
    })
