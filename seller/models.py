from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify  

class SellerProfile(models.Model):
    BUSINESS_TYPES = (
        ('individual', 'Individual/Sole Proprietor'),
        ('partnership', 'Partnership'),
        ('corporation', 'Corporation'),
        ('llc', 'LLC'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    is_approved = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=100)
    shop_slug = models.SlugField(max_length=100, unique=True, blank=True)
    shop_description = models.TextField(blank=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES, default='individual')
    business_phone = models.CharField(max_length=20)
    business_email = models.EmailField()
    business_address = models.TextField()
    tax_id = models.CharField(max_length=50, blank=True)
    shop_logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True)
    shop_banner = models.ImageField(upload_to='shops/banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.shop_name} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.shop_slug:
            self.shop_slug = slugify(self.shop_name)
        super().save(*args, **kwargs)

