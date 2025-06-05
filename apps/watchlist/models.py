from django.db import models
from django.conf import settings
from apps.job.models import Job
from apps.common.models.base_models import DateColumns


class Watchlist(DateColumns):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )
    
