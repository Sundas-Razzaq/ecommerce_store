from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SellerProfile
from .forms import SellerProfileForm, ProductForm
from products.models import Product
from checkout.models import OrderItem
from django.utils import timezone

@login_required
def become_seller(request):
    # Check if user already has seller profile
    if hasattr(request.user, 'seller_profile'):
        messages.info(request, 'You already have a seller account!')
        return redirect('seller:dashboard')
    
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            seller_profile = form.save(commit=False)
            seller_profile.user = request.user
            seller_profile.save()
            messages.success(request, 'Seller profile created successfully!')
            return redirect('seller:dashboard')
        else:
            print("Form errors during creation:", form.errors)
    else:
        initial = {'business_email': request.user.email}
        form = SellerProfileForm(initial=initial)
    
    return render(request, 'seller/seller_profile.html', {
        'form': form,
        'is_initial_setup': True
    })

@login_required
def seller_dashboard(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become_seller')
    
    seller_profile = get_object_or_404(SellerProfile, user=request.user)
    total_products = Product.objects.filter(seller=seller_profile).count()
    total_orders = 0
    total_earnings = 0
    
    return render(request, 'seller/seller_dashboard.html', {
        'seller_profile': seller_profile,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_earnings': total_earnings
    })

@login_required
def edit_seller_profile(request):
    seller_profile = get_object_or_404(SellerProfile, user=request.user)
    
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES, instance=seller_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('seller:dashboard')
        else:
            print("Form errors during update:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SellerProfileForm(instance=seller_profile)
    
    return render(request, 'seller/seller_profile.html', {
        'form': form,
        'is_initial_setup': False
    })

@login_required
def add_product(request):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You need to complete seller profile first.")
        return redirect('seller:profile')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('seller:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'seller/add_product.html', {'form': form})

@login_required
def product_list(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:profile')
    
    products = Product.objects.filter(seller=request.user.seller_profile)
    return render(request, 'seller/product_list.html', {'products': products})

@login_required
def edit_product(request, product_id):
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You need to complete seller profile first.")
        return redirect('seller:profile')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' not in request.FILES:
                form.instance.image = product.image
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('seller:product_list')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'seller/edit_product.html', {
        'form': form,
        'product': product
    })
@login_required
def delete_product(request, product_id):  
    if not hasattr(request.user, 'seller_profile'):
        messages.error(request, "You need to complete seller profile first.")
        return redirect('seller:profile')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('seller:product_list')
    
    return render(request, 'seller/delete_product.html', {'product': product})

@login_required
def seller_orders(request):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become_seller')
    
    seller = request.user.seller_profile
    order_items = OrderItem.objects.filter(seller=seller).select_related(
        'order', 'product', 'order__user'
    ).order_by('-order__created_at')
    
    return render(request, 'seller/orders.html', {
        'order_items': order_items,
        'seller': seller
    })

@login_required
def update_order_status(request, item_id):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become_seller')
    
    order_item = get_object_or_404(OrderItem, id=item_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        tracking_number = request.POST.get('tracking_number', '')
        
        if new_status in dict(OrderItem.ITEM_STATUS).keys():
            order_item.status = new_status
            order_item.tracking_number = tracking_number
            
            if new_status == 'S':  # Shipped
                order_item.shipped_at = timezone.now()
            elif new_status == 'C':  # Completed
                order_item.completed_at = timezone.now()
            
            order_item.save()
            messages.success(request, "Order status updated successfully")
        else:
            messages.error(request, "Invalid status")
    
    return redirect('seller:seller_orders')

@login_required
def update_shipping_price(request, item_id):
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become_seller')
    
    order_item = get_object_or_404(OrderItem, id=item_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        try:
            shipping_price = float(request.POST.get('shipping_price', 0))
            order_item.shipping_price = shipping_price
            order_item.save()
            messages.success(request, "Shipping price updated successfully")
        except ValueError:
            messages.error(request, "Invalid shipping price")
    
    return redirect('seller:seller_orders')
