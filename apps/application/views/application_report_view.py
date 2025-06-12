from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest
)
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from apps.application.models.application import Application
from apps.application.utils.filters import (
    normalize_text,
    normalize_jobname_expression,
)
from apps.application.utils.reports import (
    generate_pdf_report,
    generate_xlsx_report,
)


@login_required
def application_report_view(request):
    """
    Generate a report (PDF or XLSX) of filtered/sorted applications.
    Accepts the same filters as the application_list_view.
    """
    status = request.GET.get("status")
    jobname = request.GET.get("jobname")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    sort = request.GET.get("sort")
    report_type = request.GET.get("type", "pdf").lower()

    queryset = (
        Application.objects
        .filter(user=request.user)
        .select_related("job")
    )

    if status:
        queryset = queryset.filter(status=status)

    if jobname:
        normalized_input = normalize_text(jobname)
        queryset = queryset.annotate(
            normalized_jobname=normalize_jobname_expression("job__job_name")
        ).filter(normalized_jobname__icontains=normalized_input)

    if date_from:
        queryset = queryset.filter(applied_date__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(applied_date__date__lte=date_to)

    allowed_sorts = {
        "status",
        "created_at",
        "job__job_name",
        "job__company_name",
    }
    if sort in allowed_sorts:
        queryset = queryset.order_by(sort)
    else:
        queryset = queryset.order_by("-created_at")

    columns = [_("Job Name"), _("Company"), _("Status"), _("Application Date")]
    data = [
        (
            app.job.job_name,
            app.job.company_name,
            _(app.get_status_display()),
            app.applied_date.strftime("%d %B %Y")
            if app.applied_date else "",
        )
        for app in queryset
    ]

    if report_type == "pdf":
        html_string = render_to_string(
            "application_report.html",
            {
                "applications": queryset,
                "columns": columns,
            }
        )
        return generate_pdf_report(html_string)

    if report_type == "xlsx":
        return generate_xlsx_report(data, columns)

    return HttpResponseBadRequest(
        _("Invalid report type requested. Use 'pdf' or 'xlsx'.")
    )

