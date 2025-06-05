from django.db import models
from django.conf import settings
from apps.job.models import Job

class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(auto_now_add=True)
