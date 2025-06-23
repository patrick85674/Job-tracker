from django.urls import path

from apps.watchlist.views import (
    watchlist_partial,
    add_job_to_watchlist,
    partial_remove_view,
    watchlist_edit_view,
    watchlist_edit_modal_view,
    watchlist_add_modal_view
)


app_name = "watchlist"


urlpatterns = [
    path("partial/", watchlist_partial, name="watch_list_partial"),
    path("add/", add_job_to_watchlist, name="add_job_to_watchlist"),
    path(
        "watchlist_partial_remove/<int:id>",
        partial_remove_view,
        name="watchlist_partial_remove",
    ),
    path(
        "watchlist_edit/<int:id>",
        watchlist_edit_view,
        name="watchlist_edit",
    ),
    path(
        "edit/<int:id>/modal/",
        watchlist_edit_modal_view,
        name="watchlist_edit_modal",
    ),
    path("add/modal/", watchlist_add_modal_view, name="watchlist_add_modal"),
]
