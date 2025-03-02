from store import models as store_models
from django.db.models import Count, Min, Max

def default(request):
    products = store_models.Product.objects.filter(status='Published')
    categories = store_models.Category.objects.all()
    return {
        'products': products,
        'categories': categories,
    }