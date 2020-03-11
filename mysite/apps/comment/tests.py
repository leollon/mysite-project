import random
import string

from django.db.utils import DataError
from django.test import TestCase
from django.urls import reverse
from utils import cache

from .models import Comment

from apps.article.models import Article  # noqa: isort:skip
from apps.category.models import ArticleCategory  # noqa: isort:skip
from apps.user.models import User  # noqa: isort:skip


class TestCaseBase(TestCase):

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


class TestArticleCommentListAPIView(TestCaseBase):

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

        # post with correct email address
        cache.set(key='jkll9', value='jkll9', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'wrong email', 'comment_text': 'wrong email address',
                'email': 'good@email.com', 'captcha': 'jkll9', 'post': self.article.id})
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'email', status_code=201)

        # post with correct link
        cache.set(key='akll9', value='akll9', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'wrong email', 'comment_text': 'wrong email address',
                'email': 'good@email.com', 'captcha': 'akll9', 'post': self.article.id,
                'link': 'http://a.b.com'})
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'link', status_code=201)

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
                'username': 'wrong email', 'comment_text': 'wrong email address',
                'email': 'bad.email.com', 'captcha': 'jkll9', 'post': self.article.id})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'email', status_code=400)

        # post without correct link
        cache.set(key='akll9', value='akll9', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'wrong email', 'comment_text': 'wrong email address',
                'email': 'email@email.edu', 'captcha': 'akll9', 'post': self.article.id,
                'link': 'a.b.com'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'link', status_code=400)

        # post with too long email address
        cache.set(key='jklla', value='jklla', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'wrong email', 'comment_text': 'wrong email address',
                'email': 'adfdaddsdgood@efejijaldlkmail.com', 'captcha': 'jklla', 'post': self.article.id})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'email', status_code=400)

        # post with too long link
        cache.set(key='jklla', value='jklla', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'wrong email', 'comment_text': 'wrong email address',
                'email': 'good@email.com', 'captcha': 'jklla', 'post': self.article.id,
                'link': 'http://a1343jifjldsajflkjsadljfsd.b.eomcmmejsk'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'link', status_code=400)

        # post with too long comment text
        cache.set(key='abifej', value='jfiejls', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'commentor', 'comment_text': ''.join([s for _ in range(500) for s in random.choice(string.printable)]),
                'post': self.article.id, 'link': 'http://a.b.eomcmmejsk', 'captcha': 'abifej'})
        self.assertContains(response, "comment_text", status_code=400)

        # post with too long username
        cache.set(key='abifed', value='32sdS', timeout=30)
        response = self.http_client.post(
            reverse('api:article_comment_list', args=(self.article.slug,)),
            data={
                'username': 'cfeodafdmmentorfjeijiodsajhfhde32cfeodafdmmentorfjeijiodsajhfhde32',
                'comment_text': 'too long username', 'post': self.article.id,
                'link': 'http://a.b.eomcmmejsk', 'captcha': 'abifed'})
        self.assertContains(response, "username", status_code=400)


class TestCommentModel(TestCaseBase):

    def test_create_comment_success(self):
        comment = Comment.objects.create(
            username='halo', comment_text='halo leaves a comment',
            post=self.article,
        )

        self.assertIn('halo', str(comment))
        self.assertEqual(
            reverse('api:article_detail', args=(self.article.slug,)), comment.get_absolute_url())

        comment = Comment.objects.create(
            username='hello', comment_text='hello leaves a comment again',
            post=self.article,
        )

        self.assertIn('hello', str(comment))
        self.assertEqual(
            reverse('api:article_detail', args=(self.article.slug,)), comment.get_absolute_url())

    def test_create_comment_failure_with_too_long_link(self):

        # too long link
        try:
            Comment.objects.create(
                username='commentor', comment_text='commentor leaves a comment',
                post=self.article, link='http://a1343jifjldsajflkjsadljfsd.b.eomcmmejsk')
        except DataError:
            self.assertRaises(DataError)

    def test_create_comment_failure_with_too_long_email_address(self):

        # too long email address
        try:
            Comment.objects.create(
                username='commentor', comment_text='commentor leaves a comment',
                post=self.article, link='http://a1343jifjldsajflkjsadljfsd.b.eomcmmejsk')
        except DataError:
            self.assertRaises(DataError)

    def test_create_comment_failure_with_too_long_comment_text(self):

        # too long comment text
        try:
            Comment.objects.create(
                username='commentor', comment_text=''.join([s for _ in range(500) for s in random.choice(string.printable)]),
                post=self.article, link='http://a1343jifjldsajflkjsadljfsd.b.eomcmmejsk')
        except DataError:
            self.assertRaises(DataError)

    def test_create_comment_failure_with_too_long_username(self):

        # too long username
        try:
            Comment.objects.create(
                username='mmentorfjeijladjfljasefjdsafjsafds', comment_text=''.join([s for _ in range(500) for s in random.choice(string.printable)]),
                post=self.article, link='http://a1343jifjldsajflkjsadljfsd.b.eomcmmejsk')
        except DataError:
            self.assertRaises(DataError)
