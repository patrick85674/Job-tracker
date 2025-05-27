from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.watchlist.models import Watchlist


@login_required
def watchlist_partial(request):
    query = request.GET.get("q", "").strip()
    watchlist_items = Watchlist.objects.filter(user=request.user).select_related("job")

    if query:
        watchlist_items = watchlist_items.filter(
            Q(job__job_name__icontains=query) |
            Q(job__job_description__icontains=query)
        )

    return render(request, "partials/watchlist_list.html", {"watchlist_items": watchlist_items})
