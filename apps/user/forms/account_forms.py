from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


# ----------------- Email Change Form -----------------
class EmailChangeForm(forms.ModelForm):
    """
    Allows users to update their email address with confirmation and
    password verification.
    """
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
        """
        Pop custom user instance for validation and reuse in clean().
        """
        self.user = kwargs.pop('instance')
        super().__init__(*args, instance=self.user, **kwargs)

    def clean(self):
        """
        Validate email match and verify current password.
        """
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        password = cleaned_data.get("password")

        if email and confirm_email and email != confirm_email:
            self.add_error("confirm_email", "Emails do not match.")

        if password and not self.user.check_password(password):
            self.add_error("password", "Incorrect current password.")

        return cleaned_data


# ----------------- Custom Password Change Form -----------------
class CustomPasswordChangeForm(PasswordChangeForm):
    """ Custom form that inherits from Django’s PasswordChangeForm and adds
        placeholder text to the input field, without changing backend logic.

    """
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


# ----------------- Delete Account Form -----------------
class DeleteAccountForm(forms.Form):
    """
    Simple form for confirming account deletion by password input.
    """
    password = forms.CharField(
        label="Enter your password to confirm:",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )