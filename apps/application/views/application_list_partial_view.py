from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.application.models import application


@login_required
def application_list_partial(request):
    query = request.GET.get("q", "").strip()
    application_items = application.objects.filter(
        user=request.user
    ).select_related("job")

    if query:
        application_items = application_items.filter(
            Q(job__job_name__icontains=query)
            | Q(job__job_description__icontains=query)
        )

    return render(
        request,
        "partials/application_list_partial.html",
        {"application_items": application_items},
    )
