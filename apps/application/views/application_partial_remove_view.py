from apps.application.views.application_remove_view import (
    application_remove_view,
)
from apps.application.views.application_list_partial_view import (
    application_list_partial,
)
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404


@login_required
def partial_remove_view(request, id):
    # Deletes item in the application list
    application_remove_view(request, id)
    # Update partial list
    return application_list_partial(request)
