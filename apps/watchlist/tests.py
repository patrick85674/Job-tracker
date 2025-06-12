from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now

from apps.job.models import Job
from apps.watchlist.models import Watchlist


class TestWatchlist(TestCase):
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
        self.watchjob = Watchlist.objects.create(
            user=self.user,
            job=self.job,
        )

    def test_model_creation(self):
        self.assertIsNotNone(self.watchjob)

    def test_relations_exist(self):
        self.assertEqual(self.watchjob.job, self.job)
        self.assertEqual(self.watchjob.user, self.user)

    def test_default_values(self):
        self.assertIsNotNone(self.watchjob.created_at)
        delta = abs((now() - self.watchjob.created_at).total_seconds())
        self.assertLess(delta, 5)
        self.assertIsNotNone(self.watchjob.updated_at)
        delta = abs((now() - self.watchjob.updated_at).total_seconds())
        self.assertLess(delta, 5)

    def test_cascade_delete_job(self):
        job_id = self.job.id
        watchjob_id = self.watchjob.id
        self.job.delete()
        self.assertFalse(Job.objects.filter(id=job_id).exists())
        self.assertFalse(Watchlist.objects.filter(id=watchjob_id).exists())

    def test_cascade_delete_user(self):
        User = get_user_model()
        user_id = self.user.id
        watchjob_id = self.watchjob.id
        self.user.delete()
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertFalse(Watchlist.objects.filter(id=watchjob_id).exists())

    def test_reverse_relation(self):
        self.assertIn(self.watchjob, self.job.watchlist_set.all())
