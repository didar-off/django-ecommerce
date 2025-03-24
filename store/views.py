from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from decimal import Decimal
from django.db.models import Q, Avg, Sum
from django.contrib import messages

from store import models as store_models
from customer import models as customer_models
from plugin.tax_calculation import tax_calculation
from plugin.service_fee import calculate_service_fee


def index(request):
    products = store_models.Product.objects.filter(status='Published')

    context = {
        'products': products
    }

    return render(request, 'store/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(store_models.Product, status='Published', slug=slug)
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
        if weight:
            existing_cart_items.weight = weight
        if color:
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


def cart(request):
    
    if 'cart_id' in request.session:
        cart_id = request.session['cart_id']
    else:
        cart_id = None

    items = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user) if request.user.is_authenticated else Q(cart_id=cart_id))
    cart_sub_total = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user) if request.user.is_authenticated else Q(cart_id=cart_id)).aggregate(sub_total = Sum('sub_total'))['sub_total']

    try:
        addresses = customer_models.Address.objects.filter(user=request.user)
    except:
        addresses = None

    if not items:
        messages.warning(request, 'Ypur cart is empty. Start shopping with us!')
    
    context = {
        'items': items,
        'cart_sub_total': cart_sub_total,
        'addresses': addresses
    }

    return render(request, 'store/cart.html', context)


def clear_cart_items(request):
    try:
        cart_id = request.session['cart_id']
        store_models.Cart.objects.filter(cart_id=cart_id).delete()
    except:
        pass

    return


def delete_cart_item(request):
    id = request.GET.get('id')
    item_id = request.GET.get('item_id')
    cart_id = request.GET.get('cart_id')

    if not id or not item_id or not cart_id:
        return JsonResponse({'error': 'Item or Product Id not found'}, status=400)
    
    try:
        product = store_models.Product.objects.get(status='Published', id=id)
    except store_models.Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    store_models.Cart.objects.filter(product=product, id=item_id).delete()

    total_cart_items = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user)).count()
    cart_sub_total = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user)).aggregate(sub_total=Sum('sub_total'))['sub_total']

    return JsonResponse({
        'message': 'Item Deleted',
        'total_cart_items': total_cart_items,
        'cart_sub_total': '{:,.2f}'.format(cart_sub_total) if cart_sub_total else "0.00"
    })


def search(request):
    query = request.GET.get('query', '').strip()
    products = store_models.Product.objects.none()

    if query:
        products = store_models.Product.objects.filter(name__icontains=query, status='Published').order_by('-date')

    context = {
        'products': products,
        'query': query
    }

    return render(request, 'store/search.html', context)


def create_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')

        if not address_id:
            messages.warning(request, 'Please select an adress to continue')
            return redirect('store:cart')
        
        address = customer_models.Address.objects.filter(user=request.user, id=address_id).first()

        if 'cart_id' in request.session:
            cart_id = request.session['cart_id']
        else:
            cart_id = None

        items = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user) if request.user.is_authenticated else Q(cart_id=cart_id))
        cart_sub_total = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user) if request.user.is_authenticated else Q(cart_id=cart_id)).aggregate(sub_total=Sum('sub_total'))['sub_total']
        cart_shipping_total = store_models.Cart.objects.filter(Q(cart_id=cart_id) | Q(user=request.user) if request.user.is_authenticated else Q(cart_id=cart_id)).aggregate(shipping=Sum('shipping'))['shipping']

        order = store_models.Order()
        order.sub_total = cart_sub_total
        order.customer = request.user
        order.address = address
        order.shipping = cart_shipping_total
        order.tax = tax_calculation(address.country, cart_sub_total)
        order.total = order.sub_total + order.shipping + Decimal(order.tax)
        order.service_fee = calculate_service_fee(order.total)
        order.total += order.service_fee
        # order.initial_total = order.total
        order.save()

        for i in items:
            store_models.OrderItem.objects.create(
                order = order,
                product = i.product,
                qty = i.qty,
                color = i.color,
                weight = i.weight,
                price = i.price,
                sub_total = i.sub_total,
                shipping = i.shipping,
                tax = tax_calculation(address.country, i.sub_total),
                total = i.total,
                initial_total = i.total,
                vendor = i.product.vendor
            )

            order.vendors.add(i.product.vendor)

    return redirect('store:checkout', order.order_id)


def checkout(request, order_id):
    order = store_models.Order.objects.get(order_id=order_id)

    context = {
        'order': order
    }

    return render(request, 'store/checkout.html', context)


def coupon_apply(request, order_id):

    try:
        order = store_models.Order.objects.get(order_id=order_id)
        order_items = store_models.OrderItem.objects.filter(order=order)
    except store_models.Order.DoesNotExist:
        return redirect('store:checkout')
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        if not coupon_code:
            messages.error(request, 'No coupon entered')
            return redirect('store:checkout', order.order_id)
        
        try:
            coupon = store_models.Coupon.objects.get(code=coupon_code)
        except store_models.Coupon.DoesNotExist:
            messages.error(request, "Coupon does not exist")
            return redirect('store:checkout', order.order_id)
        
        if coupon in order.coupons.all():
            messages.error(request, 'Coupon already activated')
            return redirect('store:checkout', order.order_id)
        else:
            total_discount = 0

            for item in order_items:
                if coupon.vendor == item.product.vendor and coupon not in item.coupon.all():
                    item_discount = item.total * coupon.discount / 100
                    total_discount += item_discount

                    item.coupon.add(coupon)
                    item.total -= item_discount
                    item.saved += item_discount
                    item.save()

            if total_discount > 0:
                order.coupons.add(coupon)
                order.total -= total_discount
                order.sub_total -= total_discount
                order.saved += total_discount
                order.save()

        messages.success(request, 'Coupon activated')
        return redirect('store:checkout', order.order_id)


def order_verify(request, order_id):
    order = store_models.Order.objects.get(order_id=order_id)
    if request.method == 'POST':
        payment_method = 'Cash'
        if order.payment_status == 'Processing':
            order.payment_status = 'Paid'
            order.payment_method = payment_method
            order.save()
            clear_cart_items(request)
            return redirect(f'/payment-status/{order.order_id}/?payment-status=Paid')
    else:
        order.payment_status = 'Failed'
        order.save()
        return redirect(f'/payment-status/{order.order_id}/?payment-status=Failed')
    

def payment_status(request, order_id):
    order = store_models.Order.objects.get(order_id=order_id)
    payment_status = request.GET.get('payment_status')

    context = {
        'order': order,
        'payment_status': payment_status
    }

    return render(request, 'store/payment-status.html', context)