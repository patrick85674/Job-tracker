from datetime import datetime, timedelta
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.application.models.application import Application
from apps.job.models import Job
from apps.watchlist.models import Watchlist

from .sample_data import job_titles, company_names, locations, job_descriptions
from .sample_data import contact_names, phone_numbers, comments


start_date: datetime = datetime(2021, 1, 1)
end_date: datetime = datetime(2025, 4, 30)


def random_datetime(start: datetime, end: datetime) -> datetime:
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )


@login_required
def add_sample_data_view(request):

    for i in range(50):
        created_at = random_datetime(start_date, end_date)
        updated_at = created_at + timedelta(days=random.randint(0, 365))
        job_name = job_titles[i]
        company_name = company_names[i]
        location = random.choice(locations)
        link = f"https://example.com/job/{i+1}"
        job_description = job_descriptions[i]

        contact_name = contact_names[i]
        contact_email = f"user{i+1}@example.com"
        contact_phone = phone_numbers[i]
        comment = comments[i]
        status = random.choice(Application.StatusType.choices)[0]
        platform = random.choice(Application.PlatformType.choices)[0]

        job = Job.objects.create(
            user=request.user,
            job_name=job_name,
            link=link,
            job_description=job_description,
            company_name=company_name,
            location=location,
            created_at=created_at,
            updated_at=updated_at,
        )
        # calling update() is required to change updated_at
        Job.objects.filter(pk=job.pk).update(updated_at=updated_at)
        app = Application.objects.create(
            user=request.user,
            job=job,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            status=status,
            platform=platform,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at,
        )
        Application.objects.filter(pk=app.pk).update(updated_at=updated_at)
        watchjob = Watchlist.objects.create(
            user=request.user,
            job=job,
            created_at=created_at,
            updated_at=updated_at,
        )
        Watchlist.objects.filter(pk=watchjob.pk).update(updated_at=updated_at)

    return HttpResponse(
        f"Added sample data ({i+1} jobs, applications and watchlist elements)!"
    )
