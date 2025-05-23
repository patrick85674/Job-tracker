from django.urls import path
from .views import (
    RegisterView,
    CustomLoginView,
    logout_view,
    home_view,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home_view, name="home"),
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
]
