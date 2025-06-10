from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Value
from django.db.models.functions import Lower, Replace
from django.shortcuts import render

from apps.application.models.application import Application

NUMBER_OF_LISTED_APPLICATIONS = 25


@login_required
def application_list_view(request):
    # Start with applications belonging to the current user and fetch related 
    # job data
    queryset = (
        Application.objects.filter(user=request.user)
        .select_related("job")
        .order_by("-created_at")  # Default order: newest first
    )

    # Extract filters from the GET request
    status = request.GET.get("status")
    jobname = request.GET.get("jobname")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    sort = request.GET.get("sort")

    # Filter by application status (e.g. "accepted", "pending", etc.)
    if status:
        queryset = queryset.filter(status=status)

    if jobname:
        """
        Normalize both the user input and job_name by:
        - converting to lowercase
        - replacing hyphens and en-dashes with spaces
        This ensures "backend", "back-end", and "back end" all match each other
        """
        normalized_input = (
            jobname.lower()
            .replace("-", " ")
            .replace("–", " ")
        )
        queryset = queryset.annotate(
            normalized_jobname=Replace(
                Replace(Lower("job__job_name"), Value("-"), Value(" ")),
                Value("–"), Value(" "),
            )
        ).filter(normalized_jobname__icontains=normalized_input)

    # Filter by application date range
    if date_from:
        queryset = queryset.filter(applied_date__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(applied_date__date__lte=date_to)

    # Sorting by allowed fields only
    allowed_sorts = {
        "status",
        "created_at",
        "job__job_name",
        "job__company_name",
    }
    if sort in allowed_sorts:
        queryset = queryset.order_by(sort)

    # Paginate the results
    paginator = Paginator(queryset, NUMBER_OF_LISTED_APPLICATIONS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Send context to the template: results, filters, and choices 
    # for the filter dropdown
    context = {
        "page_obj": page_obj,
        "filters": {
            "status": status or "",
            "jobname": jobname or "",
            "date_from": date_from or "",
            "date_to": date_to or "",
            "sort": sort or "",
        },
        "status_choices": Application.StatusType.choices,
    }

    return render(request, "application_list.html", context)
