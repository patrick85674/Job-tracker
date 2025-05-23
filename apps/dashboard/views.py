from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.job.models import Job


@login_required
def dashboard_home(request):
    jobs = Job.objects.filter(user=request.user)

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "jobs": jobs,
        },
    )


@login_required
def job_list_partial(request):
    query = request.GET.get("q", "").strip()

    jobs = Job.objects.filter(user=request.user)

    if query:
        jobs = jobs.filter(job_name__icontains=query) | jobs.filter(
            job_description__icontains=query
        )

    return render(request, "partials/job_list.html", {"jobs": jobs})
