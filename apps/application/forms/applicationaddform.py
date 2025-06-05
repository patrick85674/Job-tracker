from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from apps.application.models.application import Application


class ApplicationAddForm(forms.ModelForm):
    status = forms.TypedChoiceField(
        required=False,
        choices=Application.status_type.choices,
        initial=Application.status_type.DRAFT,
        label=_("Status"),
        coerce=int,
    )
    applied_date = forms.DateTimeField(
        required=False,
        label=_("Applied date"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    contact_name = forms.CharField(
        max_length=Application.MAX_CONTACT_NAME_LENGTH,
        required=False,
        label=_("Contact name"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter the name...")}),
    )
    contact_email = forms.EmailField(
        # max_length=Application.MAX_EMAIL_LENGTH,
        max_length=Application._meta.get_field("contact_email").max_length,
        required=False,
        label=_("Contact E-Mail"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter the E-Mail...")}),
    )
    contact_phone = PhoneNumberField(
        required=False,
        label=_("Contact phone number"),
        widget=forms.TextInput(attrs={"placeholder": ("Enter the number...")}),
    )
    platform = forms.TypedChoiceField(
        required=False,
        choices=Application.platform_type.choices,
        initial=Application.platform_type.NONE,
        label=_("Platform"),
        coerce=int,
    )
    comment = forms.CharField(
        max_length=Application.MAX_COMMENT_LENGTH,
        required=False,
        label=_("Comment"),
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a comment...")}
        ),
    )

    class Meta:
        model = Application
        fields = ["status", "applied_date", "contact_name",
                  "contact_email", "contact_phone", "platform", "comment"]
