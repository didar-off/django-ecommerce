from django.urls import path
from vendor import views

app_name = 'vendor'

urlpatterns = [
    path('vendor-list/', views.vendor_list, name='vendor-list'),
    path('vendor-detail/<slug>/', views.vendor_detail, name='vendor-detail'),
]
