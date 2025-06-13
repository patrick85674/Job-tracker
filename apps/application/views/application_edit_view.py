from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.job.forms import JobAddForm


@login_required
def application_edit_view(request, id):
    application = get_object_or_404(Application, id=id)
    if application.user != request.user:
        return HttpResponseForbidden(
            _("No permission to change this application!"))

    if request.method == "POST":
        appform = ApplicationAddForm(request.POST, instance=application)
        jobform = JobAddForm(request.POST, instance=application.job)

        if appform.is_valid() and jobform.is_valid():
            jobform.save()
            appform.save()

            context = {}

            return render(request, "application_edited.html", context)
    else:
        appform = ApplicationAddForm(None, instance=application)
        jobform = JobAddForm(None, instance=application.job)

    context = {}
    context["jobform"] = jobform
    context["appform"] = appform

    return render(request, "application_edit.html", context)
