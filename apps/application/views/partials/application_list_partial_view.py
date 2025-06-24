from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from apps.application.models.application import Application
from apps.dashboard.constants import DASHBOARD_APPLICATION_LIMIT


@login_required
def application_list_partial(request):
    query = request.GET.get("q", "").strip()
    application_items = Application.objects.filter(
        user=request.user
    ).select_related("job")

    if query:
        application_items = application_items.filter(
            Q(job__job_name__icontains=query)
            | Q(job__job_description__icontains=query)
        )
    application_items = application_items[:DASHBOARD_APPLICATION_LIMIT]

    return render(
        request,
        "partials/application_list_partial.html",
        {"application_items": application_items},
    )
