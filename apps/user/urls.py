
from django.urls import path
from apps.user.views.auth_views import RegisterView, HomeView, logout_view
from apps.user.views.account_views import AccountPageView, DeleteAccountView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


urlpatterns = [
    path("login/", LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name='register'),

    # Password reset URLs
    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="password_reset_form.html"
         ),
         name="password_reset"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset_done.html"
         ),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset_confirm.html"
         ),
         name="password_reset_confirm"),
    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_complete.html"
         ),
         name="password_reset_complete"),

    # Account page URLs
    path("account/", AccountPageView.as_view(), name="account_page"),
    path("account/delete/", DeleteAccountView.as_view(),
         name="account_delete"),
    path(
        "account/deleted/",
        TemplateView.as_view(
            template_name="account_deleted_confirmation.html"
        ),
        name="account_deleted",
    ),

]
