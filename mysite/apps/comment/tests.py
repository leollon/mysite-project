from apps.article.models import Article  # noqa isort: skip
from apps.category.models import ArticleCategory  # noqa isort: skip
from apps.user.models import User  # noqa isort: skip
from django.test import TestCase
from django.urls import reverse
from utils import cache


class TestArticleCommentListAPIView(TestCase):

    def setUp(self) -> None:
        self.http_client = self.client_class()
        user = User.objects.create_user(
            username='commentor', email='commentor@mail.com',
            password='commentoradji'
        )
        category = ArticleCategory.objects.create(name='test-comment')

        self.article = Article.objects.create(
            title='abcd',
            article_body='test comment',
            author=user,
            category=category
        )

    def test_request_success(self):

        response = self.http_client.get(
            reverse('api:article_comment_list', args=('abcd',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')), 0)

        cache.set(key='1zk4', value='1zk4', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=('abcd',)),
            data={
                'username': 'hello', 'comment_text': 'comment content',
                'post': self.article.id, 'captcha': '1zk4'})
        self.assertContains(response, 'hello', status_code=201)
        self.assertContains(response, 'comment content', status_code=201)

    def test_request_failure(self):

        # post without captcha
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'abcdef', 'comment_text': 'comment content2',
                'post': self.article.id, 'captcha': ''})
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Invalid captcha', status_code=404)

        # post without correct article
        cache.set(key='abc93', value='abc999', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'abcdef', 'comment_text': 'comment content2',
                'post': 99, 'captcha': 'abc93'})
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'not exist', status_code=404)

        # post without correct email address
        cache.set(key='jkll9', value='jkll9', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': "wrong email", 'comment_text': "wrong email address",
                'email': "bad.email.com", 'captcha': 'jkll9', 'post': self.article.id})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'email', status_code=400)
