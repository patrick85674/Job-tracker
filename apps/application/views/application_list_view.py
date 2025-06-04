from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.application.models.application import Application

NUMBER_OF_LISTED_APPLICATIONS: int = 25


@login_required
def application_list_view(request):

    application_list = Application.objects.filter(
        user__id=request.user.id).all().select_related("job")
    paginator = Paginator(application_list, NUMBER_OF_LISTED_APPLICATIONS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {}
    context["page_obj"] = page_obj

    return render(request, "application_list.html", context)
