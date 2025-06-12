from django.urls import path

from apps.testapp.views import add_sample_data_view


urlpatterns = [
    path("add_sample_data/", add_sample_data_view, name="add_sample_data_view"),
]
