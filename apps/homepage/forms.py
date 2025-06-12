from django import forms
from .models import EmailSubscription

class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email Address'
            }),
        }
