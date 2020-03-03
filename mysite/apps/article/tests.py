from io import StringIO
from json import loads as json_loads

from django.core.management import call_command
from django.test import Client as HTTPClient
from django.test import TestCase
from django.urls import reverse

from apps.user.models import User  # noqa isort:skip


class APIViewTestCaseBase(TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()
        User.objects.create_user(username="root", email="email@test.com", password="admin1234")


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

    def test_visit_an_article(self):

        # HTTP GET
        response = self.http_client.get(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 404)
        assert isinstance(response.data, dict)

        # import test article data
        out = StringIO()
        call_command('importmd', stdout=out)

        # HTTP GET
        response = self.http_client.get(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 200)
        assert isinstance(response.data, dict)
        self.assertEqual(response.data.get("title").lower(), "hello world")

        # HTTP PUT
        response = self.http_client.put(
            reverse("api:article_detail", args=("hello-world",)),
            data={"title": "hello world", "article_body": "new article content.", "author": 1, "category": 1})
        self.assertEqual(response.status_code, 405)

        # HTTP PATCH
        response = self.http_client.patch(
            reverse("api:article_detail", args=("hello-world",)),
            data={"title": "hello world", "article_body": "new article content patch."})
        self.assertEqual(response.status_code, 405)

        # HTTP DELETE
        response = self.http_client.delete(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 405)

        # HTTP HEAD
        response = self.http_client.head(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 405)

        # HTTP OPTIONS
        response = self.http_client.options(reverse("api:article_detail", args=("hello-world",)))
        self.assertEqual(response.status_code, 200)


class TestTagListAPIView(APIViewTestCaseBase):

    def test_visit_tag_list(self):

        # HTTP GET
        response = self.http_client.get(reverse("api:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content.decode('utf-8'), "tags")
        response_content = json_loads(response.content.decode('utf-8'))
        self.assertGreaterEqual(response_content.get("count"), 0)
        self.assertGreaterEqual(len(response_content.get("tags")), 0)
        self.assertIsNone(response_content.get("tags").get("notes"))

        # HTTP POST
        response = self.http_client.post(reverse("api:tag_list"), data={"name": "test_tag_name"})
        self.assertEqual(response.status_code, 405)

        # HTTP HEAD
        response = self.http_client.head(reverse("api:tag_list"))
        self.assertEqual(response.status_code, 405)

        # HTTP OPTIONS
        response = self.http_client.options(reverse("api:tag_list"))
        self.assertEqual(response.status_code, 200)


class TestTaggedArticleListAPIView(APIViewTestCaseBase):

    def test_visit_tagged_article_list(self):

        # HTTP GET
        response = self.http_client.get(reverse("api:tagged_articles", args=("untagged",)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), len(response.data.get("results")))
        assert isinstance(response.data.get("results"), list)

        # HTTP POST
        response = self.http_client.post(
            reverse("api:tagged_articles", args=("unttaged",)),
            data={
                "title": "unttaged_article_title", "article_body": "untagged_article_body", "author": 1, "category": 1})
        self.assertEqual(response.status_code, 405)
