from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
        
        
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


def logout_view(request):
    logout(request)
    return redirect('login')