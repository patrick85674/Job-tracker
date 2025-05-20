from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.application.models.application import Application

NUMBER_OF_RECENT_APPLICATIONS: int = 10


@login_required
def application_home_view(request):

    recent_application_list = Application.objects.filter(
        user__id=request.user.id
    ).order_by("updated_at")[:NUMBER_OF_RECENT_APPLICATIONS]

    context = {}
    context["recent_applications"] = recent_application_list

    return render(request, "application_home.html", context)
