from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    # HomePage & Display Products 
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product-detail/<slug>/', views.product_detail, name='product-detail'),
    path('product-detail/<slug>/', views.product_detail, name='product-detail'),

    # Display Categories
    path('categories/', views.categories, name='categories'),
    path('category-products/<slug>/', views.category_products, name='category-products'),

    # Display Vendors
    path('vendors/', views.vendors, name='vendors'),
    path('vendor-detail/<slug>/', views.vendor_detail, name='vendor-detail'),
]
