from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
)
from django.utils.translation import gettext_lazy as _


# ----------------- Registration Form -----------------
class UserRegisterForm(UserCreationForm):
    """
    Custom user registration form extending Django's UserCreationForm.
    Adds email field with uniqueness check and Bootstrap styling.
    """
    username = forms.CharField(
        label=_("Username"),
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Choose a username"),
        })
    )

    email = forms.EmailField(
        label=_("Email Address"),
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter your email address"),
        })
    )

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Create a password")
        }),
        help_text=password_validators_help_text_html()
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Confirm your password"),
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """
        Ensure the email is unique across all users.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("A user with this email address already exists.")
            )
        return email
