from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, logout
from django.utils.translation import gettext_lazy as _
from apps.user.forms import EmailChangeForm, CustomPasswordChangeForm
from apps.user.forms import DeleteAccountForm


# ----------------- Account Page View -----------------
class AccountPageView(LoginRequiredMixin, View):
    """
    Handles both email and password changes on a single account page.
    Uses two separate forms: EmailChangeForm and CustomPasswordChangeForm.
    """
    def get(self, request):
        email_form = EmailChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'account_page.html', {
            'email_form': email_form,
            'password_form': password_form,
        })

    def post(self, request):
        # Handle email update
        if 'email_submit' in request.POST:
            email_form = EmailChangeForm(
                data=request.POST,
                instance=request.user
            )
            password_form = CustomPasswordChangeForm(user=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(
                    request,
                    _("The email address has been successfully updated.")
                )
                return redirect('account_page')
            
        # Handle password update
        elif 'password_submit' in request.POST:
            password_form = CustomPasswordChangeForm(
                user=request.user,
                data=request.POST
            )
            email_form = EmailChangeForm(instance=request.user)
            if password_form.is_valid():
                user = password_form.save()
                # Prevents logout after password change
                update_session_auth_hash(request, user)
                messages.success(
                    request,
                    _("Your password has been successfully updated.")
                )
                return redirect('account_page')

        # If form is invalid or no recognized submit button was pressed
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
                form.add_error(
                    'password',
                    _("The password entered is incorrect.")
                )

        return render(request, 'account_delete.html', {'form': form})
