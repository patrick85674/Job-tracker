from django.urls import path

from apps.application.views.application_add_view import application_add_view
from apps.application.views.application_list_view import application_list_view
from apps.application.views.application_home_view import application_home_view
from apps.application.views.application_remove_view import (
    application_remove_view
)


urlpatterns = [
    path("", application_home_view, name="application_home"),
    path("application_list/", application_list_view, name="application_list"),
    path("application_add/", application_add_view, name="application_add"),
    path("application_remove/<int:id>",
         application_remove_view, name="application_remove"),
]
