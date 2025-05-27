from django.urls import path
from . import views


app_name = "watchlist"


urlpatterns = [
    path("partial/", views.watchlist_partial, name="watch_list_partial"),
]
