from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.application.views.application_add_view import (
    application_add_view,
)
from apps.application.views.application_list_partial_view import (
    application_list_partial,
)


@login_required
def partial_add_view(request):
    application_add_view(request)
    return application_list_partial(request)
