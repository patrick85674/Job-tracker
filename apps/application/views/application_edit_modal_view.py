from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.dashboard.constants import DASHBOARD_APPLICATION_LIMIT
from apps.job.forms import JobAddForm


@login_required
def application_edit_modal_view(request, id):
    """Handles Post and get request for the edit modal"""

    application = get_object_or_404(Application, id=id)
    if application.user != request.user:
        return HttpResponseForbidden(
            _("No permission to change this application!")
        )

    if request.method == "POST":
        appform = ApplicationAddForm(request.POST, instance=application)
        jobform = JobAddForm(request.POST, instance=application.job)

        if appform.is_valid() and jobform.is_valid():
            jobform.save()
            appform.save()

            context = {}

            # Return updated Application list partial so HTMX can update the page
            application_items = (
                Application.objects.filter(user=request.user)
                .order_by("-updated_at")
                .select_related("job")[:DASHBOARD_APPLICATION_LIMIT]
            )
            context = {"application_items": application_items}
            return render(
                request,
                "partials/application_list_partial.html",
                context,
            )
    else:
        appform = ApplicationAddForm(None, instance=application)
        jobform = JobAddForm(None, instance=application.job)

    context = {
        "jobform": jobform,
        "appform": appform,
        "application": application,
    }

    return render(request, "partials/application_edit_modal.html", context)
