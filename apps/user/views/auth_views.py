from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from apps.user.forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin


# ----------------- Registration View -----------------
class RegisterView(FormView):
    """
    Handles user registration using a custom UserRegisterForm.
    Automatically logs in the user after successful registration.
    """
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy("dashboard:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


# ----------------- Homepage View -----------------
class HomeView(LoginRequiredMixin, TemplateView):
    """
    Displays the home page for authenticated users.
    """
    template_name = "home.html"


# ----------------- Logout View -----------------
def logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    return redirect('login')
