from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
@require_POST
def add_entry(request):
    entry_text = request.POST.get('entry')
    if entry_text:
        entries.append(entry_text)
        return HttpResponse(f'<li>{entry_text}</li>')
    return HttpResponse(status=400)