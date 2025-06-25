from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem, Wishlist

@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('product')
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_items_count': cart.total_items,
            'product_name': product.title,
            'quantity': quantity,
            'product_image': product.image.url if product.image else '',
            'subtotal': cart_item.subtotal,
            'cart_total': cart.total_price
        })
    
    messages.success(request, f"{quantity}x {product.title} added to your cart")
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart'))

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )
    product_name = cart_item.product.title
    cart = cart_item.cart
    cart_item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_items_count': cart.total_items,
            'cart_total': cart.total_price,
            'message': f"{product_name} removed from cart"
        })
    
    messages.success(request, f"{product_name} removed from your cart")
    return redirect('cart:cart')

@require_POST
@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        pk=item_id,
        cart__user=request.user
    )
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            cart_item.delete()
            messages.success(request, "Item removed from cart")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantity updated successfully")
        
        return redirect('cart:cart')
    
    except ValueError:
        messages.error(request, "Invalid quantity entered")
        return redirect('cart:cart')

@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'cart/wishlist.html', {
        'wishlist_items': wishlist_items
    })

@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if product is already in wishlist
    in_wishlist = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).exists()
    
    if in_wishlist:
        # Remove from wishlist
        Wishlist.objects.filter(
            user=request.user,
            product=product
        ).delete()
        action = 'removed'
        in_wishlist = False
    else:
        # Add to wishlist
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
        action = 'added'
        in_wishlist = True
    
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'action': action,
            'in_wishlist': in_wishlist,
            'wishlist_count': wishlist_count,
            'product_id': product_id
        })
    
    messages.success(request, f"Product {action} from wishlist")
    return redirect(request.META.get('HTTP_REFERER', 'cart:wishlist'))