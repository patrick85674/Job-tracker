from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
)
from django.contrib.auth import password_validation


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )

    email = forms.EmailField(
        label="Email",
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        }),
        help_text=password_validators_help_text_html()
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "A user with this email already exists."
            )
        return email
       

class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label="New Email",
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new email'
        })
    )
    confirm_email = forms.EmailField(
        label="Confirm New Email",
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new email'
        })
    )
    password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        }),
        help_text="Enter your current password to confirm the change."
    )

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super().__init__(*args, instance=self.user, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        password = cleaned_data.get("password")

        if email and confirm_email and email != confirm_email:
            self.add_error("confirm_email", "Emails do not match.")

        if password and not self.user.check_password(password):
            self.add_error("password", "Incorrect current password.")

        return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password'
        })
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )