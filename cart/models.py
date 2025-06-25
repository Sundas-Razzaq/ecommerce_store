from django.db import models
from django.conf import settings
from django.db.models import F, Sum
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"

    def __str__(self):
        return f"Cart #{self.pk} - {self.user.username}"

    @property
    def total_items(self):
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def total_price(self):
        return self.items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0

    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.title} in {self.cart}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            self.quantity = 1
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.title} in {self.user.username}'s wishlist"