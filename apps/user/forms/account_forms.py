from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# ----------------- Email Change Form -----------------
class EmailChangeForm(forms.ModelForm):
    """
    Allows users to update their email address with confirmation and
    password verification.
    """
    email = forms.EmailField(
        label=_("New Email Address"),
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter new email address"),
        })
    )
    confirm_email = forms.EmailField(
        label=_("Confirm New Email Address"),
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _("Confirm new email address"),
        })
    )
    password = forms.CharField(
        label=_("Current Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter current password"),
        }),
        help_text=_("Enter your current password to confirm the change.")
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
            self.add_error("confirm_email", _("Email addresses do not match."))

        if password and not self.user.check_password(password):
            self.add_error(
                "password",
                _("The password you entered is incorrect.")
            )

        return cleaned_data


# ----------------- Custom Password Change Form -----------------
class CustomPasswordChangeForm(PasswordChangeForm):
    """ Custom form that inherits from Django’s PasswordChangeForm and adds
        placeholder text to the input field, without changing backend logic.

    """
    old_password = forms.CharField(
        label=_("Current Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter current password"),
        })
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Enter new password"),
        })
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _("Confirm new password"),
        })
    )


# ----------------- Delete Account Form -----------------
class DeleteAccountForm(forms.Form):
    """
    Simple form for confirming account deletion by password input.
    """
    password = forms.CharField(
        label=_("Enter your password to confirm:"),
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
