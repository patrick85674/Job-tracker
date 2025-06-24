from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render

from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.dashboard.constants import (
    DASHBOARD_APPLICATION_LIMIT,
    DASHBOARD_WATCHLIST_LIMIT,
)
from apps.job.forms import JobAddForm
from apps.watchlist.models import Watchlist


@login_required
def application_add_from_job_modal_view(request, id):
    """Converts a watchlist item into an application."""

    # Get the WatchlistItem, not Application
    watchlist_item = get_object_or_404(Watchlist, id=id)

    if watchlist_item.user != request.user:
        return HttpResponseForbidden(
            _("No permission to change this watchlist item!")
        )

    job = watchlist_item.job

    if request.method == "POST":
        appform = ApplicationAddForm(request.POST)
        jobform = JobAddForm(request.POST, instance=job)

        if appform.is_valid() and jobform.is_valid():
            job = jobform.save(commit=False)
            job.user = request.user
            job.save()

            application = appform.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()

            # Remove the watchlist item after creating the application
            watchlist_item.delete()

            # Fetch both updated lists
            application_items = (
                Application.objects.filter(user=request.user)
                .order_by("-updated_at")
                .select_related("job")[:DASHBOARD_APPLICATION_LIMIT]
            )

            watchlist_items = (
                Watchlist.objects.filter(user=request.user)
                .order_by("-updated_at")
                .select_related("job")[:DASHBOARD_WATCHLIST_LIMIT]
            )

            watchlist_html = render_to_string(
                "partials/watchlist_list.html",
                {"watchlist_items": watchlist_items},
                request=request,
            )

            application_html = render_to_string(
                "partials/application_list_partial.html",
                {"application_items": application_items},
                request=request,
            )
            # Render both lists
            response_html = (
                f'<div id="watch-list" hx-swap-oob="true">{watchlist_html}</div>'
                f'<div id="application-list" hx-swap-oob="true">{application_html}</div>'
            )
            return HttpResponse(response_html)

    else:
        # GET request — show prefilled form
        appform = ApplicationAddForm(initial={"job": job})
        jobform = JobAddForm(instance=job)

    context = {
        "appform": appform,
        "jobform": jobform,
        "watchlist_item": watchlist_item,
    }

    return render(
        request, "partials/application_add_from_job_modal.html", context
    )
