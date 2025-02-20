from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product-detail/<slug>/', views.product_detail, name='product-detail'),
]
