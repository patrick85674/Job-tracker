from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from apps.application.models.application import Application


class ApplicationAddForm(forms.ModelForm):
    position_title = forms.CharField(
        max_length=Application.MAX_POSITION_TITLE_LENGTH,
        required=False,
        label=_("Position title"),
    )
    company_name = forms.CharField(
        max_length=Application.MAX_COMPANY_NAME_LENGTH,
        required=False,
        label=_("Company name"),
    )
    job_link = forms.URLField(
        # max_length=Application.MAX_URL_LENGTH,
        max_length=Application._meta.get_field("job_link").max_length,
        required=False,
        label=_("Job link"),
    )
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
    )
    job_description = forms.CharField(
        widget=forms.Textarea,
        max_length=Application.MAX_DESCRIPTION_LENGTH,
        required=False,
        label=_("Job description"),
    )
    contact_name = forms.CharField(
        max_length=Application.MAX_CONTACT_NAME_LENGTH,
        required=False,
        label=_("Contact name"),
    )
    contact_email = forms.EmailField(
        # max_length=Application.MAX_EMAIL_LENGTH,
        max_length=Application._meta.get_field("contact_email").max_length,
        required=False,
        label=_("Contact E-Mail"),
    )
    contact_phone = PhoneNumberField(
        required=False,
        label=_("Contact phone number"),
    )
    platform = forms.TypedChoiceField(
        required=False,
        choices=Application.platform_type.choices,
        initial=Application.platform_type.NONE,
        label=_("Platform"),
        coerce=int,
    )
    comment = forms.CharField(
        widget=forms.Textarea,
        max_length=Application.MAX_COMMENT_LENGTH,
        required=False,
        label=_("Comment"),
    )

    class Meta:
        model = Application
        fields = ["position_title", "company_name", "job_link", "status",
                  "applied_date", "job_description", "contact_name",
                  "contact_email", "contact_phone", "platform", "comment"]
