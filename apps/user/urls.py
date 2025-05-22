from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
]
