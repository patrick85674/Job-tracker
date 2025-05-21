from django.views.generic import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


def home_view(request):
    return HttpResponse("Homepage coming soon.")


class RegisterView(FormView):
    template_name = 'user/register.html'
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