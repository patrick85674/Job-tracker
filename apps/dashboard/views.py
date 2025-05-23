from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.job.models import Job


@login_required
def dashboard_home(request):
    jobs = Job.objects.filter(user=request.user)

    print(f"Jobs for user: {jobs}")  # Log to check the jobs
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

    print(f"Filter query: {query}")  # Log the filter query

    jobs = Job.objects.filter(user=request.user)
    
    if query:
        jobs = jobs.filter(job_name__icontains=query) | jobs.filter(
            job_description__icontains=query
        )

    print(f"Jobs after filter: {jobs}")  # Log the filtered jobs
    print(f"Query: '{query}', Total jobs returned: {jobs.count()}")

    return render(request, "partials/job_list.html", {"jobs": jobs})
