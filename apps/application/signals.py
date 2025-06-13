from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.application.models.application import Application
from apps.watchlist.models import Watchlist


@receiver(post_delete, sender=Application)
@receiver(post_delete, sender=Watchlist)
def delete_orphaned_job(sender, instance, **kwargs):
    job = instance.job

    if job:
        # Check if any other models are still using this job
        application_using = Application.objects.filter(job=job).exists()
        watchjob_using = Watchlist.objects.filter(job=job).exists()

        if not application_using and not watchjob_using:
            job.delete()
