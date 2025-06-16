from django.test import TestCase
from django.urls import reverse


class TestApplicationURLReverse(TestCase):
    def test_application_add_reverse(self):
        url = reverse("application:application_add")
        self.assertEqual(url, "/application/add/")

    def test_application_edit_reverse(self):
        url = reverse("application:application_edit", kwargs={"id": 1})
        self.assertEqual(url, "/application/edit/1")

    def test_application_list_reverse(self):
        url = reverse("application:application_list")
        self.assertEqual(url, "/application/list/")

    def test_application_remove_reverse(self):
        url = reverse("application:application_remove", kwargs={"id": 1})
        self.assertEqual(url, "/application/remove/1")
