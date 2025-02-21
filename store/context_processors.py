from store import models as store_models
from django.db.models import Count, Min, Max

def default(request):
    categories = store_models.Category.objects.all()[:4]

    min_max_price = store_models.Product.objects.aggregate(Min('price'), Max('price'))

    try:
        cart_id = request.session['cart_id']
        total_cart_items = store_models.Cart.objects.filter(cart_id=cart_id).count()
    except:
        total_cart_items = 0

    return {
        'total_cart_items': total_cart_items,
        'categories': categories,
        'min_max_price': min_max_price,
    }