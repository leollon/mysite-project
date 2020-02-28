from django.db.utils import IntegrityError
from django.test import Client as HTTPClient
from django.test import TestCase
from django.urls import reverse

from .models import ArticleCategory


class TestArticleCategoryModel(TestCase):

    def test_category_intergrity(self):
        category_name = "test_category"
        try:
            ArticleCategory.objects.create(name=category_name)
        except IntegrityError:
            raise
        self.assertRaises(IntegrityError)

    def test_category_article_statistics(self):
        category_name = "abcd*())*"
        category = ArticleCategory.objects.create(name=category_name)

        self.assertEqual(category.article_statistics, 0)

        try:
            category.article_statistics = 1
        except NotImplementedError:
            self.assertRaises(NotImplementedError)

    def test_category_with_punctuation(self):
        category_name = "random#*&@#(*&R#@"
        result = "random-R-"
        self.assertEqual(ArticleCategory.objects.create(name=category_name).name, result)

    def test_category_with_japanese(self):
        category_name = "qote''彼の弟は何ですか？　。・￥、"
        result = "qote-彼の弟は何ですか-"
        self.assertEqual(ArticleCategory.objects.create(name=category_name).name, result)

    def test_category_with_chinese(self):
        category_name = "这是用Django + nextjs 写出来的博客"
        result = "这是用Django-nextjs-写出来的博客"
        self.assertEqual(ArticleCategory.objects.create(name=category_name).name, result)


class CategoryAPIViewBase(TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()


class TestArticleCategoryAPIView(CategoryAPIViewBase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()

    def test_categtories_list(self):

        response = self.http_client.get(reverse("api:category_list"))
        self.assertEqual(response.status_code, 200)

        response = self.http_client.post(reverse("api:category_list"), data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.put(reverse("api:category_list"), data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.patch(reverse("api:category_list"), data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.delete(reverse("api:category_list"), data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.get("/api/v1/categories/hello-world/")
        self.assertEqual(response.status_code, 404)

        response = self.http_client.post("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.put("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.patch("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.delete("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)


class TestCategorizedArticleListAPIView(CategoryAPIViewBase):

    def test_get_categorized_article_list(self):

        response = self.http_client.get(
            reverse("api:categorized_articles", args=("Sams-Teach-yourself-TCPIP-in-24-hours",)))
        assert len(response.data.get("results")) >= 0
        self.assertEqual(response.status_code, 200)

        response = self.http_client.get(
            reverse("api:categorized_articles", args=("undefined",)))
        self.assertEqual(response.data.get("results"), [])
        assert len(response.data.get("results")) >= 0
        self.assertEqual(response.status_code, 200)

        response = self.http_client.get(
            reverse("api:categorized_articles", args=("undefined",)), data={"name": "WhatDoUThink"})
        self.assertEqual(response.status_code, 200)

        response = self.http_client.post(reverse("api:category_list"), data={"name": "WhatDoUThink"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.post(reverse("api:category_list"), data={"name": "WhatDoUThink"})
        self.assertEqual(response.status_code, 405)
