from django import forms
from .models import SellerProfile
from products.models import Product, Category

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = [
            'shop_name', 'shop_description', 'business_type',
            'business_phone', 'business_email', 'business_address',
            'tax_id', 'shop_logo', 'shop_banner'
        ]
        widgets = {
            'shop_description': forms.Textarea(attrs={'rows': 3}),
            'business_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_email'].required = True
        self.fields['business_phone'].required = True

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'image', 'price', 'quantity', 'description', 
            'brand', 'category', 'gender', 'is_featured',
            'is_new', 'is_trending'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        self.fields['title'].required = True
        self.fields['price'].required = True
        self.fields['quantity'].required = True
        self.fields['description'].required = True
        self.fields['image'].required = True