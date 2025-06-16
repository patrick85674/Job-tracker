from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.job.forms import JobAddForm


class TestJobForm(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="customuser",
            password="password123",
            email="user@example.com"
        )
        self.valid_form_data = {
            "job_name":
                "Senior Backend Systems Architect for Scalable Python "
                "Services and Asynchronous API Ecosystems",
            "link": "https://example.com",
            "job_description":
                "We’re looking for a Senior Backend Architect to design "
                "and lead the development of scalable, asynchronous Python "
                "services and API ecosystems. You'll define architecture "
                "for high-performance backend systems, build robust async "
                "APIs using frameworks like FastAPI or aiohttp, and work "
                "with technologies such as Kafka, Redis Streams, PostgreSQL, "
                "and Kubernetes. You’ll collaborate across teams to ensure "
                "resilience, scalability, and maintainability of distributed "
                "systems in a cloud-native environment.",
            "company_name": "Leading Technology Corporation",
            "location":
                "Krung Thep Maha Nakhon Amon Rattanakosin Mahinthara Ayuthaya "
                "Mahadilok Phop Noppharat Ratchathani Burirom Udomratchaniwet "
                "Mahasathan Amon Phiman Awatan Sathit Sakkathattiya Witsanukam"
                " Prasit",
        }

    def test_form_valid(self):
        form = JobAddForm(data={"job_name": "Test job name"})
        self.assertTrue(form.is_valid())

        form = JobAddForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = JobAddForm(data={"job_name": ""})
        self.assertFalse(form.is_valid())

        form = JobAddForm()
        self.assertFalse(form.is_valid())

    def test_form_required(self):
        form = JobAddForm()
        self.assertTrue(form.fields["job_name"].required)
        self.assertFalse(form.fields["link"].required)

    def test_form_field_widget(self):
        form = JobAddForm()
        self.assertIsInstance(form.fields["job_description"].widget,
                              forms.Textarea)

    def test_form_save(self):
        form = JobAddForm(data=self.valid_form_data)
        job = form.save(commit=False)
        job.user = self.user
        job = form.save()
        self.assertIsNotNone(job)
        self.assertEqual(job.job_name, self.valid_form_data["job_name"])
        self.assertEqual(job.link, self.valid_form_data["link"])
        self.assertEqual(job.job_description,
                         self.valid_form_data["job_description"])
        self.assertEqual(job.company_name,
                         self.valid_form_data["company_name"])
        self.assertEqual(job.location, self.valid_form_data["location"])

    def test_form_rendering(self):
        form = JobAddForm(data=self.valid_form_data)
        html = form.as_p()
        self.assertIn("<input", html)

    def test_form_has_field(self):
        form = JobAddForm(data={"job_name": "Test job name (fields)"})
        self.assertIn("job_name", form.fields)
        self.assertIn("link", form.fields)
        self.assertIn("job_description", form.fields)
        self.assertIn("company_name", form.fields)
        self.assertIn("location", form.fields)
