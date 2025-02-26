from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    # HomePage
    path('', views.index, name='index'),
]