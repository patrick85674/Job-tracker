# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.watchlist.models import Watchlist
from apps.job.forms import JobAddForm
from apps.application.models.application import Application
from apps.application.forms.applicationaddform import ApplicationAddForm


@login_required
def dashboard_home(request):
    watchlist_items = Watchlist.objects.filter(
        user=request.user
    ).select_related("job")
    job_add_form = JobAddForm()

    application_items = Application.objects.filter(
        user=request.user
    ).select_related("job")
    job_add_form = ApplicationAddForm()

    # application_items = application.objects.filter(
    #     user=request.user
    # ).select_related("job")
    # job_add_form = applicationaddform()

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "watchlist_items": watchlist_items,
            "form": job_add_form,
            "application_items": application_items,
        },
    )
