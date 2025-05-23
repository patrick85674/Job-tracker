from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from .forms import UserRegisterForm, CustomLoginForm


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    

class CustomLoginView(DjangoLoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm

    def form_valid(self, form):
        identifier = form.cleaned_data.get("username")  # Note: field name is username
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=identifier, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(
                    self.request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(self.request, user)
            self.request.session['failed_attempts'] = 0
            return redirect(self.get_success_url())
        else:
            failed_attempts = self.request.session.get('failed_attempts', 0) + 1
            self.request.session['failed_attempts'] = failed_attempts

            if failed_attempts >= 3:
                messages.error(self.request, "Too many failed attempts. Forgot your password?")
            else:
                messages.error(self.request, "Invalid username or password.")

            return self.form_invalid(form)


# class CustomLoginView(DjangoLoginView):
#     template_name = 'login.html'
#     authentication_form = CustomLoginForm

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()

#         if form.is_valid():
#             identifier = form.cleaned_data.get("identifier")
#             password = form.cleaned_data.get("password")

#             # Try authenticating with username first
#             user = authenticate(request, username=identifier, password=password)

#             if user is None:
#                 # Try to find user by email and authenticate with username
#                 try:
#                     user_obj = User.objects.get(email=identifier)
#                     user = authenticate(
#                         request,
#                         username=user_obj.username,
#                         password=password
#                     )
#                 except User.DoesNotExist:
#                     user = None

#             if user is not None:
#                 request.session['failed_attempts'] = 0
#                 login(request, user)
#                 return redirect('home')

#             # Authentication failed
#             failed_attempts = request.session.get('failed_attempts', 0) + 1
#             request.session['failed_attempts'] = failed_attempts

#             if failed_attempts >= 3:
#                 messages.error(
#                     request,
#                     "Too many failed attempts. Forgot your password?"
#                 )
#             else:
#                 messages.error(request, "Invalid username or password.")

#         return self.form_invalid(form)

#     def get_form(self, form_class=None):
#         return self.authentication_form(self.request.POST or None)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'home.html')