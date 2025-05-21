from django import forms
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
        label="Job name",
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Jobname/Position..."}
        ),
    )

    link = forms.URLField(
        label="Job link",
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter link..."}),
    )

    job_description = forms.CharField(
        label="Job description",
        max_length=2000,
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Enter a description..."}
        ),
    )
