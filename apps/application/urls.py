from django.urls import path

from apps.application.views.application_add_view import application_add_view
from apps.application.views.application_edit_view import application_edit_view
from apps.application.views.application_list_view import application_list_view
from apps.application.views.application_home_view import application_home_view
from apps.application.views.application_remove_view import (
    application_remove_view
)


urlpatterns = [
    path('', application_home_view, name="application_home"),
    path("list/", application_list_view, name="application_list"),
    path("add/", application_add_view, name="application_add"),
    path("remove/<int:id>",
         application_remove_view, name="application_remove"),
    path("edit/<int:id>",
         application_edit_view, name="application_edit"),
]
