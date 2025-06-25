from .models import Cart, Wishlist

def cart_context(request):
    context = {
        'cart_items_count': 0,
        'cart_total_price': 0,
        'recent_cart_items': [],
        'wishlist_items_count': 0 
    }
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        context.update({
            'cart_items_count': cart.total_items,
            'cart_total_price': cart.total_price,
            'recent_cart_items': cart.items.order_by('-added_at')[:3],
            'wishlist_items_count': Wishlist.objects.filter(user=request.user).count()
        })
    
    return context