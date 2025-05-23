from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("job-list/", views.job_list_partial, name="job_list_partial"),  # HTMX filter endpoint
]
