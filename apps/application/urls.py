from django.urls import path

from apps.application.views.application_add_view import application_add_view
from apps.application.views.application_edit_view import application_edit_view
from apps.application.views.application_list_view import application_list_view
from apps.application.views.application_home_view import application_home_view
from apps.application.views.application_remove_view import (
    application_remove_view,
)
from apps.application.views.application_edit_modal_view import application_edit_modal_view
from apps.application.views.application_partial_remove_view import partial_remove_view as application_partial_remove_view
from apps.application.views.application_list_partial_view import (
    application_list_partial,
)
from apps.application.views.application_add_modal_view import application_add_modal_view
app_name = "application"

urlpatterns = [
    path('', application_home_view, name="application_home"),
    path("list/", application_list_view, name="application_list"),
    path("add/", application_add_view, name="application_add"),
    path("remove/<int:id>",
         application_remove_view, name="application_remove"),
    path("edit/<int:id>",
         application_edit_view, name="application_edit"),
    path(
        "partial_remove/<int:id>",
        application_partial_remove_view,
        name="application_partial_remove",
    ),
    path("partial/", application_list_partial, name="application_list_partial"),
    path("edit/<int:id>/modal/", application_edit_modal_view, name="application_edit_modal"),
    path("add/modal/", application_add_modal_view, name="application_add_modal"),
]
