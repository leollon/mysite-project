import random
import string

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from .models import ArticleCategory

from apps.article.models import Article  # noqa isort:skip
from apps.user.models import User  # noqa isort:skip


class TestArticleCategoryModel(TestCase):

    def test_category_intergrity(self):
        category_name = 'test_category'
        try:
            ArticleCategory.objects.create(name=category_name)
        except IntegrityError:
            raise
        self.assertRaises(IntegrityError)

    def test_category_article_statisticss(self):
        category_name = 'abcd*())*'
        category = ArticleCategory.objects.create(name=category_name)

        self.assertEqual(category.article_statistics, 0)
        self.assertEqual('abcd-', str(category))

        try:
            category.article_statisticss = 1
        except AttributeError:
            self.assertRaises(AttributeError)

    def test_category_with_punctuation(self):
        category_name = 'random#*&@#(*&R#@'
        result = 'random-R-'
        self.assertEqual(ArticleCategory.objects.create(name=category_name).name, result)

    def test_category_with_japanese(self):
        category_name = "qote''彼の弟は何ですか？　。・￥、"
        result = 'qote-彼の弟は何ですか-'
        self.assertEqual(ArticleCategory.objects.create(name=category_name).name, result)

    def test_category_with_chinese(self):
        category_name = '这是用Django + nextjs 写出来的博客'
        result = '这是用Django-nextjs-写出来的博客'
        self.assertEqual(ArticleCategory.objects.create(name=category_name).name, result)


class CategoryAPIViewBase(TestCase):

    def setUp(self) -> None:
        self.http_client = self.client_class()


class TestArticleCategoryAPIView(CategoryAPIViewBase):

    def test_categtories_list(self):

        response = self.http_client.get(reverse('api:category_list'))
        self.assertEqual(response.status_code, 200)

        response = self.http_client.post(reverse('api:category_list'), data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.put(reverse('api:category_list'), data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.patch(reverse('api:category_list'), data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.delete(reverse('api:category_list'), data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.get('/api/v1/categories/hello-world/')
        self.assertEqual(response.status_code, 404)

        response = self.http_client.post('/api/v1/categories/hello-world/', data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.put('/api/v1/categories/hello-world/', data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.patch('/api/v1/categories/hello-world/', data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.delete('/api/v1/categories/hello-world/', data={'name': 'test_catetory'})
        self.assertEqual(response.status_code, 404)


class TestCategorizedArticleListAPIView(CategoryAPIViewBase):

    def generate_test_articles(self):
        category_list = ('Python', 'hello-world', 'Network', 'system-design', 'Docker')
        user = User.objects.create_user(
            username="categorizedArticlesList", email="categorize@gmail.com", password="djangopasswod")
        for _ in range(random.randint(1, 30)):
            category, _ = ArticleCategory.objects.get_or_create(name=random.choice(category_list))
            for _ in range(random.randint(1, 20)):
                Article.objects.create(
                    title=''.join(random.sample(string.printable, random.randint(10, 10))),
                    article_body=''.join(random.sample(string.printable, random.randint(5, len(string.printable)))),
                    author=user,
                    category=category)

    def test_get_categorized_article_list(self):

        # HTTP GET
        response = self.http_client.get(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )))
        self.assertEqual(len(response.data.get('results')), 0)
        self.assertEqual(response.data.get('article_statistics'), 0)
        self.assertEqual(response.status_code, 200)

        # HTTP POST
        response = self.http_client.post(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )),
            data={'username': 'commentor', 'comment_text': 'comment text', 'captcha': 'fjeisl'})
        self.assertEqual(response.status_code, 405)

        # HTTP PUT
        response = self.http_client.put(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )),
            data={'username': 'commentor', 'comment_text': 'comment text', 'captcha': 'fjeisl'})
        self.assertEqual(response.status_code, 405)

        # HTTP PATCH
        response = self.http_client.patch(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )),
            data={'username': 'commentor', 'comment_text': 'comment text', 'captcha': 'fjeisl'})
        self.assertEqual(response.status_code, 405)

        # HTTP DELETE
        response = self.http_client.delete(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )),
            data={'username': 'commentor', 'comment_text': 'comment text', 'captcha': 'fjeisl'})
        self.assertEqual(response.status_code, 405)

        # HTTP HEAD
        response = self.http_client.head(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )),
            data={'username': 'commentor', 'comment_text': 'comment text', 'captcha': 'fjeisl'})
        self.assertEqual(response.status_code, 405)

        # HTTP OPTIONS
        response = self.http_client.options(
            reverse('api:categorized_articles', args=('Sams-Teach-yourself-TCPIP-in-24-hours', )),
            data={'username': 'commentor', 'comment_text': 'comment text', 'captcha': 'fjeisl'})
        self.assertEqual(response.status_code, 200)

        # HTTP GET
        response = self.http_client.get(
            reverse('api:categorized_articles', args=('undefined', )))
        self.assertEqual(response.data.get('results'), [])
        self.assertGreaterEqual(len(response.data.get('results')), 0)
        self.assertEqual(response.data.get('article_statistics'), 0)
        self.assertEqual(response.status_code, 200)

        # HTTP GET
        try:
            response = self.http_client.get(
                reverse('api:categorized_articles', args=('', )))
        except NoReverseMatch:
            self.assertRaises(NoReverseMatch)

        # HTTP GET
        try:
            response = self.http_client.get(
                reverse('api:categorized_articles', args=(' ', )))
        except NoReverseMatch:
            self.assertRaises(NoReverseMatch)

        # HTTP GET
        self.generate_test_articles()
        category = ArticleCategory.objects.all().first()
        response = self.http_client.get(
            reverse('api:categorized_articles', args=(category.name,)))
        self.assertGreaterEqual(response.data.get('article_statistics'), 1)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data.get('results')), 1)
