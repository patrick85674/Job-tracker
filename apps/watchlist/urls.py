from django.urls import path
from . import views


app_name = "watchlist"


urlpatterns = [
    path("partial/", views.watchlist_partial, name="watch_list_partial"),
    path("add/", views.add_job_to_watchlist, name="add_job_to_watchlist"),
    path(
        "watchlist_partial_remove/<int:id>",
        views.partial_remove_view,
        name="watchlist_partial_remove",
    ),
    path(
        "watchlist_edit/<int:id>",
        views.watchlist_edit_view,
        name="watchlist_edit",
    ),
    path(
        "edit/<int:id>/modal/",
        views.watchlist_edit_modal_view,
        name="watchlist_edit_modal",
    ),
]
