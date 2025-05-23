from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Job


class JobAddForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "job_name",
            "link",
            "job_description",
        ]  # Fields from the model

    job_name = forms.CharField(
        label=_("Job name"),
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter Jobname/Position...")}
        ),
    )

    link = forms.URLField(
        label=_("Job link"),
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Enter link...")}),
    )

    job_description = forms.CharField(
        label=_("Job description"),
        max_length=2000,
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": _("Enter a description...")}
        ),
    )

    company_name = forms.CharField(
        label=_("Company name"),
        max_length=300,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter the name...")}
        ),
    )

    location = forms.CharField(
        label=_("Location"),
        max_length=300,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter the location...")}
        ),
    )
