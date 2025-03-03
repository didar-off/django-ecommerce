from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    # HomePage
    path('', views.index, name='index'),
    path('product-detail/<slug>/', views.product_detail, name='product-detail'),
    path('products/', views.products, name='products'),

    # Cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
]