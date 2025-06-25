from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
import logging

logger = logging.getLogger(__name__)

@login_required
def checkout(request):
    """Handle the checkout process"""
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        if cart.total_items == 0:
            messages.warning(request, "Your cart is empty")
            return redirect('cart:cart')
            
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty")
        return redirect('cart:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                # Create order
                order = form.save(commit=False)
                order.user = request.user
                order.cart = cart
                order.payment_method = 'COD'
                order.save()
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        seller=cart_item.product.seller,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price,
                        shipping_price=getattr(cart_item.product, 'shipping_price', 0)
                    )
                
                # Clear the cart
                cart.clear()
                
                # Handle AJAX requests
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('checkout:checkout_success', args=[order.order_number])
                    })
                
                return redirect('checkout:checkout_success', order_number=order.order_number)
                
            except Exception as e:
                logger.error(f"Order processing error: {str(e)}", exc_info=True)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': str(e),
                        'form_errors': form.errors.get_json_data() if form.errors else None
                    }, status=400)
                messages.error(request, f"Error processing order: {str(e)}")
                return redirect('checkout:checkout')
        else:
            logger.error(f"Form errors: {form.errors}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.get_json_data(),
                    'non_field_errors': form.non_field_errors()
                }, status=400)
            messages.error(request, "Please correct the errors below")
    else:
        initial_data = {
            'email': request.user.email,
            'phone_number': request.user.phone_number if hasattr(request.user, 'phone_number') else '',
            'shipping_address': getattr(request.user, 'address', '')
        }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'checkout/checkout.html', {
        'cart': cart,
        'form': form,
    })

@login_required
def checkout_success(request, order_number):
    """Display order confirmation page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'checkout/order_confirmation.html', {
        'order': order
    })

@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkout/order_history.html', {
        'orders': orders
    })

@login_required
def order_detail(request, order_number):
    """Display details of a specific order"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'checkout/order_detail.html', {
        'order': order,
        'order_items': order.items.all()
    })