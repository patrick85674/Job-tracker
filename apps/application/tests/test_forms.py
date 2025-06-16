from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.utils.functional import Promise

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.job.models import Job


class TestApplicationForm(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "status": Application.StatusType.SUBMITTED,
            "applied_date": timezone.now(),
            "contact_name": "Test name",
            "contact_email": "test@test.contacttest",
            "contact_phone": "+49 030 12345678",
            "platform": Application.PlatformType.COMPANY_WEBSITE,
            "comment": "Test comment",
        }
        User = get_user_model()
        self.user = User.objects.create_user(
            username="customuser",
            password="password123",
            email="user@example.com"
        )
        self.job = Job.objects.create(
            job_name="Test job name",
            user=self.user,
        )

    def test_form_has_field(self):
        form = ApplicationAddForm()
        self.assertIn("status", form.fields)
        self.assertIn("contact_name", form.fields)
        self.assertIn("contact_phone", form.fields)
        self.assertIn("contact_email", form.fields)
        self.assertIn("platform", form.fields)
        self.assertIn("comment", form.fields)

    def test_form_valid(self):
        form = ApplicationAddForm(data={})
        self.assertTrue(form.is_valid())

        form = ApplicationAddForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

        form = ApplicationAddForm(data={
            "status": Application.StatusType.WIDTHDRAWED,
            "applied_date": datetime(2025, 12, 24, 15, 0),
            "comment": "",
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = ApplicationAddForm(data={
            "contact_email": "test",
        })
        self.assertFalse(form.is_valid())

        form = ApplicationAddForm(data={
            "status": "test",
        })
        self.assertFalse(form.is_valid())

    def test_form_initial(self):
        form = ApplicationAddForm()
        self.assertEqual(form.fields["status"].initial,
                         Application.StatusType.DRAFT)
        self.assertEqual(form.fields["platform"].initial,
                         Application.PlatformType.NONE)

    def test_form_field_widget(self):
        form = ApplicationAddForm()
        self.assertIsInstance(form.fields['comment'].widget,
                              forms.Textarea)

    def test_form_field_labels(self):
        form = ApplicationAddForm()
        # self.assertIsInstance(form.fields["contact_name"].label, str)
        # check for lazy object
        self.assertIsInstance(form.fields["contact_name"].label, Promise)

    def test_form_save(self):
        form = ApplicationAddForm(data=self.valid_form_data)
        app = form.save(commit=False)
        app.job = self.job
        app.user = self.user
        app = form.save()
        self.assertIsNotNone(app)

    def test_form_rendering(self):
        form = ApplicationAddForm(data=self.valid_form_data)
        html = form.as_p()
        self.assertIn("<input", html)
