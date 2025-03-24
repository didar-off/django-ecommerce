from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    # HomePage
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),

    path('product-detail/<slug>/', views.product_detail, name='product-detail'),
    path('products/', views.products, name='products'),

    # Cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('delete-cart-item/', views.delete_cart_item, name='delete-cart-item'),

    # Checkout
    path('create-order/', views.create_order, name='create-order'),
    path('checkout/<order_id>/', views.checkout, name='checkout'),
    path('coupon-apply/<order_id>/', views.coupon_apply, name='coupon-apply'),
    path('order-verify/<order_id>/', views.order_verify, name='order-verify'),
    path('payment-status/<order_id>/', views.payment_status, name='payment-status'),
]