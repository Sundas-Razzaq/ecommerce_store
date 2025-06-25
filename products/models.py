from django.db import models
from seller.models import SellerProfile

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    GENDER_CHOICES = [
        ('W', 'Women'),
        ('M', 'Men'),
        ('K', 'Kids'),
        ('U', 'Unisex'),
    ]
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=100, blank=True)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='products')    # Category fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Flags
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.title