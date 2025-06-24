from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from apps.application.models.application import Application



@login_required
def application_remove_view(request, id):
    application = get_object_or_404(Application, id=id)
    if application.user != request.user:
        return HttpResponseForbidden(
            _("No permission to remove this application!")
        )
    application.delete()

    context = {}
    return render(request, "application_removed.html", context)
