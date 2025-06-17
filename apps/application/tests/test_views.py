from http import HTTPStatus

#from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase
#from django.test import Client
from django.urls import reverse
#from django.utils import timezone

from apps.application.forms.applicationaddform import ApplicationAddForm
from apps.application.models.application import Application
from apps.job.forms import JobAddForm
from apps.job.models import Job


def create_and_login_testuser(self,
                              username: str = "testuser",
                              password: str = "testpassword1234!",
                              email: str = "user@example.com",  # RFC 2606
                              ):
    User = get_user_model()

    self.user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    logged_in = self.client.login(
        username=username,
        password=password,
        email=email,
    )
    self.assertTrue(logged_in)


class TestApplicationAddView(TestCase):
    def setUp(self):
        create_and_login_testuser(self)

    def test_template_name_correct(self):
        url = reverse("application:application_add")
        response = self.client.get(path=url)
        self.assertTemplateUsed(response, "application_add.html")

    def test_form_submission_creates_object(self):
        TEST_JOB_NAME: str = "Test job name"
        TEST_COMMENT: str = "Test comment text"

        url = reverse("application:application_add")
        data = {
            "job_name": TEST_JOB_NAME,
            "comment": TEST_COMMENT,
        }
        response = self.client.post(
            path=url,
            data=data,
            # content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        job = Job.objects.get(job_name=TEST_JOB_NAME)
        app = Application.objects.get(job=job, comment=TEST_COMMENT)
        self.assertEqual(job.job_name, TEST_JOB_NAME)
        self.assertEqual(app.comment, TEST_COMMENT)

    def test_form_submission_creates_all_attributes(self):
        TEST_JOB_NAME: str = "Test job name all attr"
        TEST_COMMENT: str = "Test comment text all attr"
        TEST_CONTACT_NAME: str = "Test contact name attr all"
        TEST_EMAIL: str = "userattrall@example.com"
        TEST_PHONE: str = "+493012345678"
        TEST_STATUS: Application.StatusType = Application.StatusType.SUBMITTED
        TEST_PLATFORM: Application.PlatformType = Application.PlatformType.NONE

        url = reverse("application:application_add")
        data = {
            "job_name": TEST_JOB_NAME,
            "contact_name": TEST_CONTACT_NAME,
            "contact_email": TEST_EMAIL,
            "contact_phone": TEST_PHONE,
            "status": TEST_STATUS,
            "platform": TEST_PLATFORM,
            "comment": TEST_COMMENT,
        }
        response = self.client.post(
            path=url,
            data=data,
            # content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)  # 200
        app = Application.objects.get(job__job_name=TEST_JOB_NAME)
        self.assertEqual(app.contact_name, TEST_CONTACT_NAME)
        self.assertEqual(app.contact_email, TEST_EMAIL)
        self.assertEqual(app.contact_phone, TEST_PHONE)
        self.assertEqual(app.status, TEST_STATUS)
        self.assertEqual(app.platform, TEST_PLATFORM)

        self.assertGreaterEqual(app.id, 1)

    def test_invalid_form_shows_errors(self):
        TEST_JOB_NAME_EMPTY: str = ""
        url = reverse("application:application_add")
        data = {
            "job_name": TEST_JOB_NAME_EMPTY,
        }
        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        with self.assertRaises(Job.DoesNotExist):
            Job.objects.get(job_name=TEST_JOB_NAME_EMPTY)

        TEST_JOB_NAME: str = "Test job name err"

        data = {
            "job_name": TEST_JOB_NAME,
            "status": "Test",
        }
        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        with self.assertRaises(Job.DoesNotExist):
            Job.objects.get(job_name=TEST_JOB_NAME)

    def test_get_create_form_page(self):
        url = reverse("application:application_add")

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertIn("appform", response.context)
        self.assertIsInstance(response.context["appform"], ApplicationAddForm)

        self.assertContains(response, "<form")
        self.assertContains(response, "name=\"job_name\"")

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        url = reverse("application:application_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302


class TestApplicationEditView(TestCase):
    def setUp(self):
        create_and_login_testuser(self)

        # setup an application
        self.TEST_JOB_NAME: str = "Test job name (edit)"

        url = reverse("application:application_add")
        data = {
            "job_name": self.TEST_JOB_NAME,
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.app = Application.objects.get(job__job_name=self.TEST_JOB_NAME)
        self.assertEqual(self.app.comment, "")

    def test_edit_form_submission(self):
        TEST_CONTACT_NAME: str = "Test contact name (edit)"
        TEST_EMAIL: str = "useredit@example.com"
        TEST_PHONE: str = "+493012345678"
        TEST_STATUS: Application.StatusType = Application.StatusType.REJECTED
        TEST_PLATFORM: Application.PlatformType = (
            Application.PlatformType.COMPANY_WEBSITE
        )
        TEST_COMMENT: str = "Test comment text (edit)"
        url = reverse("application:application_edit", args=[self.app.id])
        data = {
            "job_name": self.TEST_JOB_NAME,
            "contact_name": TEST_CONTACT_NAME,
            "contact_email": TEST_EMAIL,
            "contact_phone": TEST_PHONE,
            "status": TEST_STATUS,
            "platform": TEST_PLATFORM,
            "comment": TEST_COMMENT,
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        app = Application.objects.get(job__job_name=self.TEST_JOB_NAME)
        self.assertEqual(app.comment, TEST_COMMENT)
        self.assertEqual(app.contact_name, TEST_CONTACT_NAME)
        self.assertEqual(app.contact_email, TEST_EMAIL)
        self.assertEqual(app.contact_phone, TEST_PHONE)
        self.assertEqual(app.status, TEST_STATUS)
        self.assertEqual(app.platform, TEST_PLATFORM)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        url = reverse("application:application_edit", args=[self.app.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302


class TestApplicationListView(TestCase):
    def setUp(self):
        create_and_login_testuser(self)

        # setup applications
        TEST_COMMENT: str = "Test comment text (list)"
        self.TEST_JOB_NAMES = []
        for x in range(0, 20):
            self.TEST_JOB_NAMES.append("Test job name (list) " + str(x))

        for job_name in self.TEST_JOB_NAMES:
            url = reverse("application:application_add")
            data = {
                "job_name": job_name,
                "comment": TEST_COMMENT,
            }
            response = self.client.post(path=url, data=data)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.app = Application.objects.get(job__job_name=job_name)
            self.assertEqual(self.app.comment, TEST_COMMENT)

    def test_list_applications(self):
        url = reverse("application:application_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        for job_name in self.TEST_JOB_NAMES:
            try:
                self.assertContains(response, ">" + job_name + "<")
            except AssertionError:
                self.assertContains(response, "\"" + job_name + "\"")

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        url = reverse("application:application_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302


class TestApplicationRemoveView(TestCase):
    def setUp(self):
        create_and_login_testuser(self)

        # setup an application
        self.TEST_JOB_NAME: str = "Test job name (remove)"

        url = reverse("application:application_add")
        data = {
            "job_name": self.TEST_JOB_NAME,
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.app = Application.objects.get(job__job_name=self.TEST_JOB_NAME)
        self.assertEqual(self.app.comment, "")

    def test_remove_application(self):
        url = reverse("application:application_remove", args=[self.app.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        url = reverse("application:application_remove", args=[self.app.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # 404

    def test_remove_application_wrong_user(self):
        create_and_login_testuser(self,
                                  username="testwronguser",
                                  email="wronguser@example.com")
        url = reverse("application:application_remove", args=[self.app.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)  # 403

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        url = reverse("application:application_remove", args=[self.app.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302
