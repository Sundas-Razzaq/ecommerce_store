from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_view, name='view'),
    path('become-seller/', views.become_seller, name='become_seller'),
]