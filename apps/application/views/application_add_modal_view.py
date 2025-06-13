from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.dashboard.constants import DASHBOARD_APPLICATION_LIMIT
from apps.job.forms import JobAddForm


@login_required
def application_add_modal_view(request):

    if request.method == "POST":  # Try to write into database if post-request

        appform = ApplicationAddForm(request.POST)
        jobform = JobAddForm(request.POST)

        if appform.is_valid() and jobform.is_valid():
            job = jobform.save(commit=False)
            job.user = request.user
            job.save()

            app = appform.save(commit=False)
            app.user = request.user
            app.job = job
            app.save()

            context = {}
            context = {"job": job}
            context = {"application": app}

            # Return updated Application list partial so HTMX can update the page
            application_items = (
                Application.objects.filter(
                    user=request.user
                )
                .order_by("-updated_at")
                .select_related("job")[:DASHBOARD_APPLICATION_LIMIT]
            )
            return render(
                request,
                "partials/application_list_partial.html",
                {"application_items": application_items},
            )
    else:   # This will fill the modal if get-request
        jobform = JobAddForm()
        appform = ApplicationAddForm()

    context = {}
    context["jobform"] = jobform
    context["appform"] = appform

    return render(request, "partials/application_add_modal.html", context)
