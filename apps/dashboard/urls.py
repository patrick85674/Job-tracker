from django.urls import path
from . import views
from apps.watchlist import views as watchlist_views 


app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("watch-list/", watchlist_views.watchlist_partial, name="watch_list_partial"),  # HTMX filter endpoint
]
