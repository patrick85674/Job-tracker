from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views import View
from .forms import EmailChangeForm, CustomPasswordChangeForm
from .forms import DeleteAccountForm


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


# Single page for all account updates
class AccountPageView(LoginRequiredMixin, View):
    def get(self, request):
        email_form = EmailChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'account_page.html', {
            'email_form': email_form,
            'password_form': password_form,
        })
    
    def post(self, request):
        if 'email_submit' in request.POST:
            email_form = EmailChangeForm(
                data=request.POST,
                instance=request.user
            )
            password_form = CustomPasswordChangeForm(user=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully.")
                return redirect('account_page')

        elif 'password_submit' in request.POST:
            password_form = CustomPasswordChangeForm(
                user=request.user,
                data=request.POST
            )
            email_form = EmailChangeForm(instance=request.user)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully.")
                return redirect('account_page')

        else:
            email_form = EmailChangeForm(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)

        return render(
            request,
            'account_page.html',
            {
                'email_form': email_form,
                'password_form': password_form,
            }
        )


# ----------------- Delete Account View -----------------

class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request):
        form = DeleteAccountForm()
        return render(request, 'account_delete.html', {'form': form})

    def post(self, request):
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username,
                                password=password)

            if user is not None:
                user.delete()
                logout(request)
                return redirect('account_deleted')
            else:
                form.add_error('password', "Incorrect password.")
        
        return render(request, 'account_delete.html', {'form': form})