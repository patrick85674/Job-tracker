from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.watchlist.models import Watchlist
from apps.job.forms import JobAddForm
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _



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
            return current_watchlist(request)
          
        else:

            return render(request, "job/add_job_form.html", {"form": form})


def current_watchlist(request):
    watchlist_items = Watchlist.objects.filter(
        user=request.user
    ).select_related("job")
    return render(
        request,
        "partials/watchlist_list.html",
        {"watchlist_items": watchlist_items},
    )


@login_required
def watchlist_remove_view(request, id):
    watchlist = get_object_or_404(Watchlist, id=id)
    if watchlist.user != request.user:
        return HttpResponseForbidden(
            _("No permission to remove this application!")
        )
    watchlist.delete()

    context = {}
    return render(request, "watchlist_entry_removed.html", context)


# from django.shortcuts import render, redirect, get_object_or_404

@login_required
def partial_remove_view(request, id):
    # Deletes item in the watchlist
    watchlist_remove_view(request, id)
    # Update partial list
    return watchlist_partial(request)
