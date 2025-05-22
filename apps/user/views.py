from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            failed_attempts = request.session.get('failed_attempts', 0) + 1
            request.session['failed_attempts'] = failed_attempts

            if failed_attempts >= 3:
                messages.error(request, "Too many failed attempts. Forgot your password?")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login after logout


@login_required
def home_view(request):
    return render(request, "home.html")


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')  # Redirect after successful registration

    def form_valid(self, form):
        # Save user and manually assign fields
        user = form.save(commit=False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        login(self.request, user)  # Automatically log in the user
        return super().form_valid(form)