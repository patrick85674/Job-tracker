from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
     path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.subscribe_success, name='subscribe-success'),
]


