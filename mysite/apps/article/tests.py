from io import StringIO
from json import loads as json_loads
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import IntegrityError
from django.test import Client as HTTPClient
from django.test import TestCase
from django.urls import reverse

from .models import Article
from .tasks import increment_page_view_times, increment_user_view_times

from apps.user.models import User  # noqa isort:skip
from apps.category.models import ArticleCategory  # noqa isort:skip


class TestIncreUVTasks(TestCase):

    def setUp(self) -> None:

        category = ArticleCategory.objects.create(
            name="test increment user view times task")
        user = User.objects.create_user(
            username="tasks", email="tasks@gmail.com", password="taskpassed2233")
        Article.objects.create(
            title="halo world", article_body="test increment user view times",
            author=user, category=category)

    @patch('apps.article.tasks.Article.user_view_times')
    def test_increment_user_view_times(self, *args):

        article = Article.objects.get(title="halo world")

        self.assertEqual(increment_user_view_times(100), 0)
        self.assertEqual(increment_user_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title="halo world").user_view_times, 1)
        self.assertEqual(increment_user_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title="halo world").user_view_times, 2)


class TestIncrePVTasks(TestCase):

    def setUp(self) -> None:

        category = ArticleCategory.objects.create(
            name="test increment user view times task")
        user = User.objects.create_user(
            username="tasks", email="tasks@gmail.com", password="taskpassed2233")
        Article.objects.create(
            title="halo world", article_body="test increment user view times",
            author=user, category=category)

    @patch('apps.article.tasks.Article.page_view_times')
    def test_increment_page_view_times(self, *args):

        article = Article.objects.get(title="halo world")

        self.assertEqual(increment_page_view_times(100), 0)
        self.assertEqual(increment_page_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title="halo world").page_view_times, 1)
        self.assertEqual(increment_page_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title="halo world").page_view_times, 2)


class TestArticleModel(TestCase):

    def setUp(self):
        self.category = ArticleCategory.objects.create(name="test category")
        self.user = User.objects.create_user(
            username="root", email="email@gmail.com", password="admin1234")

    def test_article_integrity(self):
        title = "article integrity error"
        article_body = "```python\nimport os\nprint('article integrity error')\n"
        Article.objects.create(
            title=title, article_body=article_body, author=self.user)
        try:
            Article.objects.create(title=title, article_body=article_body, author=self.user)
        except IntegrityError:
            self.assertRaises(IntegrityError)

    def test_article_comment_statistics(self):

        title = "halo world"
        article_body = "hello world article content"
        Article.objects.create(
            title=title, article_body=article_body, author=self.user, category=self.category)
        article = Article.objects.get(slug="halo-world")
        self.assertEqual(article.comment_statistics, 0)

        try:
            article.comment_statistics = 1
        except NotImplementedError:
            self.assertRaises(NotImplementedError)

    def test_article(self):
        title = "*(#UOJFDEJ(*#@J(*#@89343"
        article_body = "hello world"
        article = Article.objects.create(
            title=title, article_body=article_body, author=self.user, category=self.category)

        # test slug
        self.assertEqual("uojfdejj89343", article.slug)
        # test category name
        self.assertEqual(self.category.name, article.category.name)
        # test article's tags
        self.assertEqual("untagged", article.tags)

        title = "-"
        article_body = "content"
        article = Article.objects.create(
            title=title, article_body=article_body, author=self.user)

        # test slug
        self.assertEqual("-", article.slug)
        # test category name
        self.assertIsNone(article.category)
        # test article's tags
        self.assertEqual("untagged", article.tags)

        # test article with author
        title = "article without author"
        article_body = "article without author"

        try:
            article = Article.objects.create(
                title=title, article_body=article, category=self.category)
        except IntegrityError:
            self.assertRaises(IntegrityError)

        # test article's tags
        tags = "J*(J#JFKE*(#@)#*#U,J*#LFJLD"
        title = "article with specified tags"
        article_body = "article with specified tags content"
        article = Article.objects.create(
            title=title, article_body=article_body, author=self.user, category=self.category,
            tags=tags
        )
        self.assertEqual("JJJFKEU,JLFJLD", article.tags)


class APIViewTestCaseBase(TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()
        User.objects.create_user(
            username="root", email="email@test.com", password="admin1234")


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
                "title": "unttaged_article_title", "article_body": "untagged_article_body",
                "author": 1, "category": 1})
        self.assertEqual(response.status_code, 405)
