from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now

from apps.application.models.application import Application
from apps.job.models import Job


class TestApplicationModel(TestCase):
    def setUp(self):
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
        self.app = Application.objects.create(
            job=self.job,
            user=self.user,
        )

    def test_default_values(self):
        app = self.app
        self.assertEqual(app.job, self.job)
        self.assertEqual(app.user, self.user)
        self.assertEqual(app.status, Application.StatusType.DRAFT)
        self.assertEqual(app.platform, Application.PlatformType.NONE)

        self.assertIsNotNone(app.created_at)
        self.assertLess(abs((now() - app.created_at).total_seconds()), 5)
        self.assertIsNotNone(app.updated_at)
        self.assertLess(abs((now() - app.updated_at).total_seconds()), 5)

    def test_attributes_are_available(self):
        self.assertTrue(hasattr(Application, "contact_name"))
        self.assertTrue(hasattr(Application, "contact_email"))
        self.assertTrue(hasattr(Application, "contact_phone"))
        self.assertTrue(hasattr(Application, "comment"))
        self.assertTrue(hasattr(Application, "status"))
        self.assertTrue(hasattr(Application, "platform"))

    def test_cascade_delete_job(self):
        User = get_user_model()
        app = self.app
        user_id = self.user.id
        job_id = self.job.id
        app_id = app.id
        self.job.delete()
        self.assertTrue(User.objects.filter(id=user_id).exists())
        self.assertFalse(Job.objects.filter(id=job_id).exists())
        self.assertFalse(Application.objects.filter(id=app_id).exists())

    def test_cascade_delete_user(self):
        User = get_user_model()
        app = self.app
        user_id = self.user.id
        job_id = self.job.id
        app_id = app.id
        self.user.delete()
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(Job.objects.filter(id=job_id).exists())
        self.assertFalse(Application.objects.filter(id=app_id).exists())

    def test_cascade_delete_app(self):
        User = get_user_model()
        app = self.app
        user_id = self.user.id
        job_id = self.job.id
        app_id = app.id
        app.delete()
        self.assertTrue(User.objects.filter(id=user_id).exists())
        self.assertFalse(Job.objects.filter(id=job_id).exists())
        self.assertFalse(Application.objects.filter(id=app_id).exists())
