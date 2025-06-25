from django.shortcuts import render
from products.models import Product
from products.models import Product, Category
from django.db.models import Q

# Create your views here.
def base_page(request):
    return render(request, 'core/home.html')

def contact_page(request):
    return render(request, 'core/contact.html')

def about_page(request):
    return render(request, 'core/about.html')

#----------------- views for the home page with featured, new arrivals, and trending products --------------------#

def home(request):
    featured_products = Product.objects.filter(is_featured=True)
    new_arrivals = Product.objects.filter(is_new=True)
    trending_products = Product.objects.filter(is_trending=True)

    return render(request, 'core/index.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'trending_products': trending_products,
    })

def search_results(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    return render(request, 'core/search_results.html', {
        'query': query,
        'results': results
    })
