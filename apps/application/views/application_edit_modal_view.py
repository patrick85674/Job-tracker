from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.job.forms import JobAddForm


@login_required
def application_edit_modal_view(request, id):
    application = get_object_or_404(Application, id=id)
    if application.user != request.user:
        return HttpResponseForbidden(_("No permission to change this application!"))

    appform = ApplicationAddForm(instance=application)
    jobform = JobAddForm(instance=application.job)

    context = {"jobform": jobform, "appform": appform, "application": application}
    return render(request, "partials/application_edit_partial.html", context)
