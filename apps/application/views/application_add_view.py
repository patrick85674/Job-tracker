from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.job.forms import JobAddForm
from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application


@login_required
def application_add_view(request):

    if request.method == "POST":
        print("Post request")
        appform = ApplicationAddForm(request.POST)
        jobform = JobAddForm(request.POST)
        if appform.is_valid() and jobform.is_valid():
            print("Form is valid!")
            job = jobform.save(commit=False)
            job.user = request.user
            job.save()

            app = appform.save(commit=False)
            app.user = request.user
            app.job = job
            app.save()
            print("Application saved!")

            context = {}
            context = {"job": job}
            context = {"application": app}
            return render(request, "application_added.html", context)

    else:
        jobform = JobAddForm()
        appform = ApplicationAddForm()

    context = {}
    context["jobform"] = jobform
    context["appform"] = appform

    return render(request, "application_add.html", context)
