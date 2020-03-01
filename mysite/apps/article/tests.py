from io import StringIO

from django.core.management import call_command
from django.test import Client as HTTPClient
from django.test import TestCase
from django.urls import reverse

from apps.user.models import User  # noqa isort:skip


class APIViewTestCaseBase(TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()
        User.objects.create(username="root", email="email@test.com", password="admin1234")


class TestArticleListAPIView(APIViewTestCaseBase):

    def test_article_list(self):

        # HTTP GET
        response = self.http_client.get(reverse("api:article_list"))
        self.assertGreaterEqual(len(response.data.get("results")), 0)

        # HTTP POST
        response = self.http_client.post(
            reverse("api:article_list"),
            data={
                "title": "halo world", "article_body": "halo world test data",
                "category": 1, "autho": 1})
        self.assertEqual(response.status_code, 405)


class TestArticleDetailAPIView(APIViewTestCaseBase):

    # HTTP GET
    def test_visit_an_article(self):

        response = self.http_client.get(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 404)

        out = StringIO()
        call_command('importmd', stdout=out)
        response = self.http_client.get(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 200)
