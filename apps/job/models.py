from django.db import models
from django.conf import settings
from apps.common.models.base_models import DateColumns

# Create your models here.
class Job(DateColumns):
    # One user many jobs
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    # Is mandatory
    job_name = models.CharField(max_length=200, null=False, blank=False)
    link = models.URLField(
        max_length=300,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now=True)
    job_description = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
    )
    company_name = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        db_index=True,
    )
    location = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        db_index=True,
    )

    def __str__(self):

        return f"{self.job_name}"

    class Meta:
        # app_name_model_name, user_user
        db_table = "job"
