"""
URL configuration for Jobtracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("apps.homepage.urls")),
    path("admin/", admin.site.urls),
    path("user/", include("apps.user.urls")),
    path("application/", include("apps.application.urls")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("watchlist/", include("apps.watchlist.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("test/", include("apps.testapp.urls")),
    ]
