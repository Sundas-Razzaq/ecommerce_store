from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),  
    path('women/', views.women_products, name='women'),
    path('men/', views.men_products, name='men'),
    path('kids/', views.kids_products, name='kids'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]

