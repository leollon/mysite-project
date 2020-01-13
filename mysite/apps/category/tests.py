from django.contrib.auth.models import AnonymousUser
from django.test import Client as HTTPClient
from django.test import RequestFactory, TestCase


class TestCategory(TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()
        self.request_factory = RequestFactory()
        self.anonymous_user = AnonymousUser()

    def test_categtories_list(self):

        response = self.http_client.get("/categories/")
        self.assertEqual(response.status_code, 200)

    def test_get_categorized_article_list(self):

        response = self.http_client.get("/categories/Sams-Teach-yourself-TCPIP-in-24-hours/")
        self.assertEqual(response.status_code, 404)

        response = self.http_client.get("/categories/hello-world/")  # unknown category name
        self.assertEqual(response.status_code, 404)
