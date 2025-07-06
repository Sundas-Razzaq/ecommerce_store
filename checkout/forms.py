from django import forms
from django.core.validators import RegexValidator
from .models import Order

class CheckoutForm(forms.ModelForm):
    accept_terms = forms.BooleanField(required=True,label="I agree to the Terms & Conditions",
        error_messages={
            'required': 'You must accept the terms and conditions'
        }
    )
    
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be 9-15 digits long and can start with +"
            )
        ]
    )
    
    class Meta:
        model = Order
        fields = ['email', 'shipping_address', 'phone_number', 'order_note']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'order_note': forms.Textarea(attrs={'rows': 2}),
        }
        error_messages = {
            'email': {
                'required': 'Please enter your email address',
                'invalid': 'Please enter a valid email address'
            },
            'shipping_address': {
                'required': 'Please enter your shipping address'
            },
            'phone_number': {
                'required': 'Please enter your phone number'
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'accept_terms':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data