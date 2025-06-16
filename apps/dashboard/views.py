# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.dashboard.constants import DASHBOARD_APPLICATION_LIMIT
from apps.dashboard.constants import DASHBOARD_WATCHLIST_LIMIT
from apps.job.forms import JobAddForm
from apps.watchlist.models import Watchlist


@login_required
def dashboard_home(request):
    watchlist_items = Watchlist.objects.filter(
        user=request.user
    ).order_by("-updated_at").select_related("job")[:DASHBOARD_WATCHLIST_LIMIT]
    job_add_form = JobAddForm()

    application_items = (
        Application.objects.filter(
            user=request.user
        )
        .order_by("-updated_at")
        .select_related("job")[:DASHBOARD_APPLICATION_LIMIT]
    )
    application_add_form = ApplicationAddForm()

    # application_items = application.objects.filter(
    #     user=request.user
    # ).select_related("job")
    # job_add_form = applicationaddform()
    context = {
            "watchlist_items": watchlist_items,
            "form": job_add_form,
            "application_items": application_items,
            "application_form": application_add_form,
            "disable_sb_forms": True,
        }
    return render(
        request,
        "dashboard/dashboard.html",
        context
    )
