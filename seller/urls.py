from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('', views.seller_dashboard, name='dashboard'),
    path('profile/', views.edit_seller_profile, name='profile'),
    path('become-seller/', views.become_seller, name='become_seller'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders/', views.seller_orders, name='seller_orders'),
    path('orders/update-status/<int:item_id>/', views.update_order_status, name='update_order_status'),
    path('orders/update-shipping/<int:item_id>/', views.update_shipping_price, name='update_shipping_price'),
]