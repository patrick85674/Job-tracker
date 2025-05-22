from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class DateColumns(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Application(DateColumns):
    MAX_POSITION_TITLE_LENGTH: int = 256
    MAX_COMPANY_NAME_LENGTH: int = 256
    # MAX_URL_LENGTH: int = 200  # django default value
    MAX_DESCRIPTION_LENGTH: int = 8192
    MAX_CONTACT_NAME_LENGTH: int = 256
    # MAX_EMAIL_LENGTH: int = 254  # django default value
    MAX_COMMENT_LENGTH: int = 8192

    class status_type(models.IntegerChoices):
        DRAFT = 1, _("Draft")
        SUBMITTED = 2, _("Submitted")
        # APPLIED = 2, _("Applied")
        # SHORTLISTED = 3, _("Shortlisted")
        INVITED = 3, _("Invited")
        REJECTED = 4, _("Rejected")
        WIDTHDRAWED = 5, _("Withdrawed")
        ACCEPTED = 6, _("Accepted")
        INTERVIEWED = 7, _("Interviewed")
        OFFERED = 8, _("Offered")

    class platform_type(models.IntegerChoices):
        NONE = 0, _("None")
        COMPANY_WEBSITE = 1, _("Company website")
        INDEED = 2, "Indeed"
        LINKEDIN = 3, "LinkedIn"

    # id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    job = models.ForeignKey(
        to="job.Job",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    position_title = models.CharField(
        max_length=MAX_POSITION_TITLE_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )
    company_name = models.CharField(
        max_length=MAX_COMPANY_NAME_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )
    job_link = models.URLField(
        # max_length=MAX_URL_LENGTH,
        null=True,
        blank=True,
    )
    status = models.PositiveIntegerField(
        default=status_type.DRAFT,
        null=True
    )
    applied_date = models.DateTimeField(
        null=True,
        blank=True
    )
    job_description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
        null=True,
        blank=True,
    )
    contact_name = models.CharField(
        max_length=MAX_CONTACT_NAME_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )
    contact_email = models.EmailField(
        # max_length=MAX_EMAIL_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )
    contact_phone = PhoneNumberField(
        null=True,
        blank=True,
        db_index=True,
    )
    platform = models.PositiveIntegerField(
        default=platform_type.NONE,
        null=True,
    )
    comment = models.TextField(
        max_length=MAX_COMMENT_LENGTH,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        db_table = "application"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "job"],
                name="u_userjob",
            )
        ]
