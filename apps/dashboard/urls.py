from django.urls import path
from . import views
from apps.watchlist import views as watchlist_views
from apps.application.views.partials import application_list_partial_view as application_views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path(
        "watch-list/",
        watchlist_views.watchlist_partial,
        name="watch_list_partial",
    ),
    path(
        "application-list/",
        application_views.application_list_partial,
        name="application_list_partial",
    ),
]
