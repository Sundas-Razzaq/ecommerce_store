from django.db import models
from django.conf import settings
from cart.models import Cart
import time

class Order(models.Model):
    ORDER_STATUS = (
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('C', 'Completed'),
        ('X', 'Cancelled')
    )
    
    PAYMENT_METHODS = (
        ('COD', 'Cash on Delivery'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    order_number = models.CharField(max_length=32, unique=True)
    email = models.EmailField()
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    order_note = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='COD')
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='P')
    is_paid = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _original_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            timestamp = int(time.time() * 1000)  
            self.order_number = f"ORD-{self.user.id}-{timestamp}"
        
        if not self.pk:  
            self._original_total = self.cart.total_price
        super().save(*args, **kwargs)

    @property
    def total(self):
        """Return the preserved total price"""
        return self._original_total if self._original_total is not None else self.cart.total_price

class OrderItem(models.Model):
    ITEM_STATUS = (
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('C', 'Completed'),
        ('X', 'Cancelled')
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey('products.Product',on_delete=models.PROTECT)
    seller = models.ForeignKey('seller.SellerProfile', on_delete=models.PROTECT, related_name='order_items', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=1, choices=ITEM_STATUS, default='P')
    tracking_number = models.CharField(max_length=100, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.quantity}x {self.product.title} (Order #{self.order.order_number})"

    @property
    def subtotal(self):
        return (self.price * self.quantity) + self.shipping_price