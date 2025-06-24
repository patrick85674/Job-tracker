from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from apps.dashboard.constants import DASHBOARD_WATCHLIST_LIMIT
from apps.job.forms import JobAddForm
from apps.watchlist.models import Watchlist


@login_required
def watchlist_partial(request):
    """
    Returns user's watchlist items based on query.
    """
    query = request.GET.get("q", "").strip()
    watchlist_items = (
        Watchlist.objects.filter(user=request.user)
        .order_by("-updated_at")
        .select_related("job")
    )

    if query:
        watchlist_items = watchlist_items.filter(
            Q(job__job_name__icontains=query)
            | Q(job__job_description__icontains=query)
        )
    watchlist_items = watchlist_items[:DASHBOARD_WATCHLIST_LIMIT]

    return render(
        request,
        "partials/watchlist_list.html",
        {"watchlist_items": watchlist_items},
    )


from django.http import HttpRequest, HttpResponse


@login_required
def add_job_to_watchlist(request: HttpRequest) -> HttpResponse:
    """
    Handle adding a job to the user's watchlist.
    """
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


def current_watchlist(request: HttpRequest) -> HttpResponse:
    """
    Render the current user's watchlist.
    """
    watchlist_items = (
        Watchlist.objects.filter(user=request.user)
        .order_by("-updated_at")
        .select_related("job")[:DASHBOARD_WATCHLIST_LIMIT]
    )
    return render(
        request,
        "partials/watchlist_list.html",
        {"watchlist_items": watchlist_items},
    )


@login_required
def watchlist_remove_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Remove a watchlist entry.
    """
    watchlist = get_object_or_404(Watchlist, id=id)
    if watchlist.user != request.user:
        return HttpResponseForbidden(
            _("No permission to remove this application!")
        )
    watchlist.delete()

    context = {}
    return render(request, "watchlist_entry_removed.html", context)


@login_required
def partial_remove_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Deletes item in the watchlist and updates partial list.
    """
    # Deletes item in the watchlist
    watchlist_remove_view(request, id)
    # Update partial list
    return watchlist_partial(request)


@login_required
def watchlist_edit_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Edit a watchlist entry.
    """
    watchlist_entry = get_object_or_404(Watchlist, id=id)
    if watchlist_entry.user != request.user:
        return HttpResponseForbidden(
            _("No permission to change this watchlist entry!")
        )

    if request.method == "POST":
        jobform = JobAddForm(request.POST, instance=watchlist_entry.job)

        if jobform.is_valid():
            jobform.save()

            return redirect("dashboard:home")
    else:
        jobform = JobAddForm(None, instance=watchlist_entry.job)

    context = {"jobform": jobform}

    return render(request, "application_edit.html", context)


@login_required
def watchlist_edit_modal_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Edit a watchlist entry in a modal.
    """
    watchlist_item = get_object_or_404(Watchlist, id=id)
    if watchlist_item.user != request.user:
        return HttpResponseForbidden(
            _("No permission to change this application!")
        )

    if request.method == "POST":
        jobform = JobAddForm(request.POST, instance=watchlist_item.job)

        if jobform.is_valid():
            jobform.save()

            # context = {}

            # Return updated Application list partial so HTMX can update the page
            watchlist_items = (
                Watchlist.objects.filter(user=request.user)
                .order_by("-updated_at")
                .select_related("job")[:DASHBOARD_WATCHLIST_LIMIT]
            )

            context = {"watchlist_items": watchlist_items}
            return render(
                request,
                "partials/watchlist_list.html",
                context,
            )
    else:
        jobform = JobAddForm(None, instance=watchlist_item.job)

    context = {
        "jobform": jobform,
        "watchlist_item": watchlist_item,
    }

    return render(request, "partials/watchlist_edit_modal.html", context)


@login_required
def watchlist_add_modal_view(request: HttpRequest) -> HttpResponse:
    """
    Add a new watchlist entry in a modal.
    """

    if request.method == "POST":  # Try to write into database if post-request

        jobform = JobAddForm(request.POST)

        if jobform.is_valid():
            job = jobform.save(commit=False)
            job.user = request.user
            job.save()

            Watchlist.objects.create(user=request.user, job=job)

            # Return updated Application list partial so HTMX can update the page
            watchlist_items = (
                Watchlist.objects.filter(user=request.user)
                .order_by("-updated_at")
                .select_related("job")[:DASHBOARD_WATCHLIST_LIMIT]
            )
            return render(
                request,
                "partials/watchlist_list.html",
                {"watchlist_items": watchlist_items},
            )
    else:  # This will fill the modal if get-request
        jobform = JobAddForm()

    context = {"jobform": jobform}
    return render(request, "partials/watchlist_add_modal.html", context)
