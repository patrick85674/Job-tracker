from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now

from apps.job.models import Job


class TestJobModel(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="customuser",
            password="password123",
            email="user@example.com"
        )

    def test_default_values(self):
        job = Job.objects.create(
            user=self.user,
            job_name="Job name test",
        )
        self.assertEqual(job.user, self.user)
        self.assertIsNotNone(job.created_at)
        self.assertLess(abs((now() - job.created_at).total_seconds()), 5)
        self.assertIsNotNone(job.updated_at)
        self.assertLess(abs((now() - job.updated_at).total_seconds()), 5)

    def test_attributes_are_available(self):
        self.assertTrue(hasattr(Job, "job_name"))
        self.assertTrue(hasattr(Job, "link"))
        self.assertTrue(hasattr(Job, "job_description"))
        self.assertTrue(hasattr(Job, "company_name"))
        self.assertTrue(hasattr(Job, "location"))

    def test_store_all_fields(self):
        TEST_JOB_NAME: str = "Job name test (store)"
        TEST_LINK: str = "https://example.com"
        TEST_JOB_DESCRIPTION: str = "Test desc (store)"
        TEST_COMPANY_NAME: str = "Test company name (store)"
        TEST_LOCATION: str = "Test location (store)"

        job = Job.objects.create(
            user=self.user,
            job_name=TEST_JOB_NAME,
            link=TEST_LINK,
            job_description=TEST_JOB_DESCRIPTION,
            company_name=TEST_COMPANY_NAME,
            location=TEST_LOCATION,
        )
        self.assertEqual(job.job_name, TEST_JOB_NAME)
        self.assertEqual(job.link, TEST_LINK)
        self.assertEqual(job.job_description, TEST_JOB_DESCRIPTION)
        self.assertEqual(job.company_name, TEST_COMPANY_NAME)
        self.assertEqual(job.location, TEST_LOCATION)
