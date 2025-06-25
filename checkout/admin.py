from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total', 'payment_method', 'is_paid', 'created_at')
    list_filter = ('status', 'payment_method', 'is_paid', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email', 'shipping_address', 'phone_number')
    readonly_fields = ('order_number', 'user', 'cart', 'created_at', 'updated_at', 'total')
    fieldsets = (
        (None, {
            'fields': ('order_number', 'user', 'cart', 'total')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'phone_number', 'email', 'order_note')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'is_paid')
        }),
        ('Status Information', {
            'fields': ('status', 'tracking_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )