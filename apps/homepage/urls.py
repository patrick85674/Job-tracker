from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('subscribe/', views.subscribe,        name='subscribe'),
    path('subscribe/success/', views.subscribe_success,name='subscribe-success'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]


