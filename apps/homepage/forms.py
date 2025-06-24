from django import forms
from django.utils.translation import gettext_lazy as _

from .models import EmailSubscription


class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': _("Email Address"),
            }),
        }
