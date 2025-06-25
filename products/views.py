from django.shortcuts import render, get_object_or_404
from .models import Product, Category

#--------------------------------------------------------#
# This view handles the product listing pages for different
#--------------------------------------------------------#
def women_products(request):
    women_products = Product.objects.filter(gender='W')
    
    footwear = women_products.filter(category__name__icontains='footwear')
    accessories = women_products.filter(category__name__icontains='accessories')
    makeup = women_products.filter(category__name__icontains='makeup')
    
    return render(request, 'products/women.html', {
        'footwear_products': footwear,
        'accessories_products': accessories,
        'makeup_products': makeup,
    })

def men_products(request):
    men_products = Product.objects.filter(gender='M')
    footwear = men_products.filter(category__name__icontains='footwear')
    watches = men_products.filter(category__name__icontains='watches')
    wallets = men_products.filter(category__name__icontains='wallets')
    return render(request, 'products/men.html', {
        'footwear_products': footwear,
        'watches_products': watches,
        'wallets_products': wallets,
    })

def kids_products(request):
    kids_products = Product.objects.filter(gender='K')
    footwear = kids_products.filter(category__name__icontains='footwear')
    clothing = kids_products.filter(category__name__icontains='clothing')
    return render(request, 'products/kids.html', {
        'footwear_products': footwear,
        'clothing_products': clothing,
        })
#----------------------------------------#
# This view handles the product detail page
#----------------------------------------#
def product_detail(request, product_id):
    print(f"Attempting to fetch product ID: {product_id}") 
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

#----------------------------------------#
# This view handles the product list page
#----------------------------------------#
def product_list(request):
    products = Product.objects.filter(quantity__gt=0)  
    
    gender = request.GET.get('gender')
    if gender in ['W', 'M', 'K']:
        products = products.filter(gender=gender)
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'title': 'All Products'
    })