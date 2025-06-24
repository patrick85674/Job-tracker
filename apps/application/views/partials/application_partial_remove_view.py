from apps.application.views.application_remove_view import application_remove_view
from apps.application.views.partials.application_list_partial_view import application_list_partial

from django.contrib.auth.decorators import login_required


@login_required
def partial_remove_view(request, id):
    # Deletes item in the application list
    application_remove_view(request, id)
    # Update partial list
    return application_list_partial(request)
