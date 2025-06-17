from django.urls import path
from . import views
from .views import faq

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.subscribe_success, name='subscribe-success'),
    path('faq/', faq, name='faq'),
]


