from django.shortcuts import render, redirect

from .forms import EmailSubscriptionForm


def homepage_view(request):
    return render(request, 'main.html')


def faq(request):
    return render(request, 'faq.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def subscribe(request):
    if request.method == "POST":
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscribe-success')
    else:
        form = EmailSubscriptionForm()
    return render(request, 'subscribe_form.html', {'form': form})


def subscribe_success(request):
    return render(request, 'subscribe_success.html')

