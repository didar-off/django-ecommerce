from store import models as store_models
from django.db.models import Q, Sum, Count


def default(request):
    cart_id = request.session.get('cart_id')
    user = request.user if request.user.is_authenticated else None

    filters = Q(cart_id=cart_id)
    if user:
        filters |= Q(user=user)

    items = store_models.Cart.objects.filter(filters)
    cart_data = items.aggregate(
        total_products=Count('id'),
        cart_sub_total=Sum('sub_total')
    )

    return {
        'total_cart_items': cart_data['total_products'] or 0,
        'items': items,
        'cart_sub_total': cart_data['cart_sub_total'] or 0.00,
    }