# products/admin.py
from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'gender', 'category')
    list_filter = ('gender', 'category', 'is_featured', 'is_new', 'is_trending')
    search_fields = ('title', 'description')

admin.site.site_header = "Your Admin Panel"