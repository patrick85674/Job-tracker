from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.watchlist.models import Watchlist
from apps.job.forms import JobAddForm
from django.http import HttpResponse


@login_required
def watchlist_partial(request):
    query = request.GET.get("q", "").strip()
    watchlist_items = Watchlist.objects.filter(
        user=request.user
    ).select_related("job")

    if query:
        watchlist_items = watchlist_items.filter(
            Q(job__job_name__icontains=query)
            | Q(job__job_description__icontains=query)
        )

    return render(
        request,
        "partials/watchlist_list.html",
        {"watchlist_items": watchlist_items},
    )


@login_required
def add_job_to_watchlist(request):
    if request.method == "GET":
        form = JobAddForm()
        return render(request, "job/add_job_form.html", {"form": form})

    if request.method == "POST":
        form = JobAddForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()

            Watchlist.objects.create(user=request.user, job=job)

            # Return updated watchlist partial so HTMX can update the page
            watchlist_items = Watchlist.objects.filter(
                user=request.user
            ).select_related("job")
            return render(
                request,
                "partials/watchlist_list.html",
                {"watchlist_items": watchlist_items},
            )
        else:
            
            return render(request, "job/add_job_form.html", {"form": form})
