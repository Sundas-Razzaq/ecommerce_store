from django.urls import path
from . import views
# Create your views here.
app_name = 'core'

urlpatterns = [
    path('', views.base_page, name='base'), 
    path('home/', views.home, name='home'), 
    path('contact/' , views.contact_page, name='contact'),
    path('about/' , views.about_page, name='about'),
    path('search/', views.search_results, name='search_results'),
]