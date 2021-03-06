import datetime
import random
import string
import tempfile
import unittest
from io import StringIO
from json import loads as json_loads
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.management.commands import flush
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from django.test.testcases import SerializeMixin
from django.urls import reverse

from .models import Article
from .tasks import increment_page_view_times, increment_user_view_times

from apps.category.models import ArticleCategory  # noqa isort:skip
from apps.user.models import User  # noqa isort:skip


class TestIncreUVTasks(TestCase):

    def setUp(self) -> None:

        category = ArticleCategory.objects.create(
            name='test increment user view times task')
        user = User.objects.create_user(
            username='tasks', email='tasks@gmail.com', password='taskpassed2233')
        Article.objects.create(
            title='halo world', article_body='test increment user view times',
            author=user, category=category)

    @patch('apps.article.tasks.Article.user_view_times')
    def test_increment_user_view_times(self, *args):

        article = Article.objects.get(title='halo world')

        self.assertEqual(increment_user_view_times(100), 0)
        self.assertEqual(increment_user_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title='halo world').user_view_times, 1)
        self.assertEqual(increment_user_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title='halo world').user_view_times, 2)


class TestIncrePVTasks(TestCase):

    def setUp(self) -> None:

        category = ArticleCategory.objects.create(
            name='test increment user view times task')
        user = User.objects.create_user(
            username='tasks', email='tasks@gmail.com', password='taskpassed2233')
        Article.objects.create(
            title='halo world', article_body='test increment user view times',
            author=user, category=category)

    @patch('apps.article.tasks.Article.page_view_times')
    def test_increment_page_view_times(self, *args):

        article = Article.objects.get(title='halo world')

        self.assertEqual(increment_page_view_times(100), 0)
        self.assertEqual(increment_page_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title='halo world').page_view_times, 1)
        self.assertEqual(increment_page_view_times(article.id), 1)
        self.assertEqual(Article.objects.get(title='halo world').page_view_times, 2)


class TestArticleModel(TestCase):

    def setUp(self):
        self.category = ArticleCategory.objects.create(name='test category')
        self.user = User.objects.create_user(
            username='root', email='email@gmail.com', password='admin1234')

    def test_article_integrity(self):
        title = 'article integrity error'
        article_body = "```python\nimport os\nprint('article integrity error')\n"
        Article.objects.create(
            title=title, article_body=article_body, author=self.user)
        try:
            Article.objects.create(title=title, article_body=article_body, author=self.user)
        except IntegrityError:
            self.assertRaises(IntegrityError)

    def test_article_comment_statistics(self):

        title = 'halo world'
        article_body = 'hello world article content'
        Article.objects.create(
            title=title, article_body=article_body, author=self.user, category=self.category)
        article = Article.objects.get(slug='halo-world')
        self.assertEqual(article.comment_statistics, 0)

        try:
            article.comment_statistics = 1
        except AttributeError:
            self.assertRaises(AttributeError)

    def test_article(self):
        title = '*(#UOJFDEJ(*#@J(*#@89343'
        article_body = 'hello world'
        article = Article.objects.create(
            title=title, article_body=article_body, author=self.user, category=self.category)

        # test slug
        self.assertEqual('uojfdejj89343', article.slug)
        # test category name
        self.assertEqual(self.category.name, article.category.name)
        # test article's tags
        self.assertEqual('untagged', article.tags)
        # test article absolute url
        self.assertURLEqual(article.get_absolute_url(), reverse('api:article_detail', args=(article.slug,)))

        title = '-'
        article_body = 'content'
        article = Article.objects.create(
            title=title, article_body=article_body, author=self.user)

        # test slug
        self.assertEqual('-', article.slug)
        # test category name
        self.assertIsNone(article.category)
        # test article's tags
        self.assertEqual('untagged', article.tags)

        # test article with author
        title = 'article without author'
        article_body = 'article without author'

        try:
            article = Article.objects.create(
                title=title, article_body=article, category=self.category)
        except IntegrityError:
            self.assertRaises(IntegrityError)

        # test article's tags
        tags = 'J*(J#JFKE*(#@)#*#U,J*#LFJLD'
        title = 'article with specified tags'
        article_body = 'article with specified tags content'
        article = Article.objects.create(
            title=title, article_body=article_body, author=self.user, category=self.category,
            tags=tags
        )
        self.assertEqual('JJJFKEU,JLFJLD', article.tags)
        # test blank article tags
        article.tags = ''
        article.save()


class APIViewTestCaseBase(TestCase):

    def setUp(self) -> None:
        self.http_client = self.client_class()
        self.user = User.objects.create_user(
            username='root', email='email@test.com', password='admin1234')


class TestArticleListAPIView(APIViewTestCaseBase):

    def test_article_list(self):

        # HTTP GET
        response = self.http_client.get(reverse('api:article_list'))
        self.assertGreaterEqual(len(response.data.get('results')), 0)

        # HTTP POST
        response = self.http_client.post(
            reverse('api:article_list'),
            data={
                'title': 'halo world', 'article_body': 'halo world test data',
                'category': 1, 'autho': 1})
        self.assertEqual(response.status_code, 405)


class TestArticleDetailAPIView(APIViewTestCaseBase):

    def test_visit_an_article(self):

        # HTTP GET
        response = self.http_client.get(reverse('api:article_detail', args=('hello-world',)))
        self.assertEqual(response.status_code, 404)
        assert isinstance(response.data, dict)

        # import test article data
        out = StringIO()
        call_command('importmd', stdout=out)
        self.assertIn('Finish importing', out.getvalue())

        # HTTP GET
        response = self.http_client.get(reverse('api:article_detail', args=('hello-world',)))
        self.assertEqual(response.status_code, 200)
        assert isinstance(response.data, dict)
        self.assertEqual(response.data.get('title').lower(), 'hello world')

        # HTTP GET
        response = self.http_client.get(reverse('api:article_detail', args=('hello-world',)))
        self.assertEqual(response.status_code, 200)
        assert isinstance(response.data, dict)
        self.assertEqual(response.data.get('title').lower(), 'hello world')

        # HTTP PUT
        response = self.http_client.put(
            reverse('api:article_detail', args=('hello-world',)),
            data={'title': 'hello world', 'article_body': 'new article content.', 'author': 1, 'category': 1})
        self.assertEqual(response.status_code, 405)

        # HTTP PATCH
        response = self.http_client.patch(
            reverse('api:article_detail', args=('hello-world',)),
            data={'title': 'hello world', 'article_body': 'new article content patch.'})
        self.assertEqual(response.status_code, 405)

        # HTTP DELETE
        response = self.http_client.delete(reverse('api:article_detail', args=('hello-world',)))
        self.assertEqual(response.status_code, 405)

        # HTTP HEAD
        response = self.http_client.head(reverse('api:article_detail', args=('hello-world',)))
        self.assertEqual(response.status_code, 405)

        # HTTP OPTIONS
        response = self.http_client.options(reverse('api:article_detail', args=('hello-world',)))
        self.assertEqual(response.status_code, 200)


class TestTagListAPIView(APIViewTestCaseBase):

    def test_visit_tag_list(self):

        # HTTP GET
        response = self.http_client.get(reverse('api:tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content.decode('utf-8'), 'tags')
        response_content = json_loads(response.content.decode('utf-8'))
        self.assertGreaterEqual(response_content.get('count'), 0)
        self.assertGreaterEqual(len(response_content.get('tags')), 0)
        self.assertIsNone(response_content.get('tags').get('notes'))

        category = ArticleCategory.objects.create(name='hello world')
        Article.objects.create(
            title='test tag list api view', article_body='tagged articles',
            author=self.user, category=category, tags='a,b,c,C')

        # HTTP GET
        response = self.http_client.get(reverse('api:tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content.decode('utf-8'), 'tags')
        response_content = json_loads(response.content.decode('utf-8'))
        self.assertGreaterEqual(response_content.get('count'), 1)
        self.assertGreaterEqual(len(response_content.get('tags')), 3)
        self.assertIsNotNone(response_content.get('tags').get('a'))

        Article.objects.create(
            title='test tag list api view 2', article_body='tagged articles 2',
            author=self.user, category=category, tags='a,b,B,c,C,,')

        # HTTP GET
        response = self.http_client.get(reverse('api:tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertRegexpMatches(response.content.decode('utf-8'), 'tags')
        response_content = json_loads(response.content.decode('utf-8'))
        self.assertGreaterEqual(response_content.get('count'), 1)
        self.assertGreaterEqual(len(response_content.get('tags')), 3)
        self.assertIsNotNone(response_content.get('tags').get('a'))

        # HTTP POST
        response = self.http_client.post(reverse('api:tag_list'), data={'name': 'test_tag_name'})
        self.assertEqual(response.status_code, 405)

        # HTTP HEAD
        response = self.http_client.head(reverse('api:tag_list'))
        self.assertEqual(response.status_code, 405)

        # HTTP OPTIONS
        response = self.http_client.options(reverse('api:tag_list'))
        self.assertEqual(response.status_code, 200)


class TestTaggedArticleListAPIView(APIViewTestCaseBase):

    def test_visit_tagged_article_list(self):

        # HTTP GET
        response = self.http_client.get(reverse('api:tagged_articles', args=('untagged',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), len(response.data.get('results')))
        assert isinstance(response.data.get('results'), list)

        # HTTP POST
        response = self.http_client.post(
            reverse('api:tagged_articles', args=('unttaged',)),
            data={
                'title': 'unttaged_article_title', 'article_body': 'untagged_article_body',
                'author': 1, 'category': 1})
        self.assertEqual(response.status_code, 405)


class TestOnlineMiddleware(TestCase):

    def setUp(self):
        category = ArticleCategory.objects.create(name='middleware test')
        user = User.objects.create_user(username='middleware', email='middleware@gmail.com', password='pa4ssmiddleware')
        self.article = Article.objects.create(
            title='online middleware test', article_body='online middleware test',
            author=user, category=category)

    def test_with_no_specified_ua(self):
        http_client = self.client_class(HTTP_USER_AGENT='Mozilla/5.0')

        response = http_client.get(reverse('api:article_detail', args=(self.article.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), self.article.title)

    def test_with_special_ua(self):
        http_client = self.client_class(HTTP_USER_AGENT='curl/7.58.0')

        response = http_client.get(reverse('api:article_detail', args=(self.article.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('title'), self.article.title)


class CommandTestBase(unittest.TestCase, SerializeMixin):
    lockfile = __file__
    out = StringIO()

    def setUp(self):

        self.temp_dir = tempfile.mkdtemp()


class TestImportmd(CommandTestBase):

    def test_import_success(self):

        call_command('importmd', stdout=self.out)
        self.assertIn('already exists', self.out.getvalue())

        # not a file
        cmd = flush.Command()
        call_command(cmd, interactive=False)
        markdown_dir = Path(settings.BASE_DIR).parent.parent.joinpath('data')
        Path(markdown_dir).joinpath('empty_dir').mkdir(exist_ok=True)
        call_command('importmd', dir='data', stdout=self.out, stderr=self.out)
        call_command(cmd, interactive=False)

    def test_import_failure(self):

        # empty directory
        try:
            call_command('importmd', dir=self.temp_dir, stdout=self.out, stderr=self.out)
        except CommandError:
            self.assertRaises(CommandError)

        # directory does not exist
        try:
            call_command('importmd', dir='a', stdout=self.out, stderr=self.out)
        except CommandError as e:
            self.assertRaises(CommandError)
            self.assertIn('a directory does not exist.', str(e.args))

        # directory without markdown files
        try:
            call_command('importmd', dir='data', stdout=self.out, stderr=self.out)
        except CommandError as e:
            self.assertRaises(CommandError)
            self.assertIn('please specify a directory containing markdown', str(e.args))

    def test_import_error(self):

        md_base_dir = self.temp_dir

        def generage_markdown_file(title, tags=['untagged']):

            article_body = ''.join([random.choice(string.printable) for __ in range(random.randint(1, 2 ** 9))])
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            hexo_markdown = (
                '---\ntitle: %s\ndate: %s\ncategories: uncategorized\ntags: %s\n---\n\n%s') % (title, date, tags, article_body)

            with open(md_base_dir + '/' + title + '.md', 'w+') as fp:
                fp.write(hexo_markdown)

        # too long title
        title = ''.join([random.choice(string.digits + string.ascii_letters) for __ in range(65)])
        generage_markdown_file(title=title)
        try:
            call_command('importmd', dir=self.temp_dir, stdout=self.out, stderr=self.out)
        except DataError as e:
            self.assertRaises(DataError)
            self.assertIn('Error, msessage', str(e))

        # too long tags
        title = ''.join([random.choice(string.digits + string.ascii_letters) for __ in range(20)])
        tags = [str(random.choice(string.digits + string.ascii_letters)) for __ in range(65)]
        generage_markdown_file(title, tags=tags)
        try:
            call_command('importmd', dir=self.temp_dir, stdout=self.out, stderr=self.out)
        except DataError as e:
            self.assertRaises(DataError)
            self.assertIn('Error, msessage', str(e))


class TestExportmd(CommandTestBase):

    def setUp(self) -> None:

        user, __ = User.objects.get_or_create(
            username='exportmd user', email='exportmd@mail.com',
            password='exportarticles')
        category, __ = ArticleCategory.objects.get_or_create(name='exportmd')
        for __ in range(10):
            Article.objects.get_or_create(
                title=''.join(random.sample(string.digits + string.ascii_letters, random.randint(2, 62))),
                article_body=''.join(random.sample(string.printable, random.randint(1, 100))),
                author=user,
                category=category)

    def test_export_success(self):

        # export all article
        call_command('exportmd', stdout=self.out)
        self.assertIn('Exported', self.out.getvalue())

        # export specified articles
        call_command(
            'exportmd', post=[article.id for article in Article.objects.all()[1:random.randint(2, 100)]], stdout=self.out)
        self.assertIn('Exported', self.out.getvalue())

    def test_export_failure(self):

        try:
            call_command('exportmd', post=[11], stdout=self.out, stderr=self.out)
        except CommandError:
            self.assertRaises(CommandError)
        self.assertIn("Not exists the article corresponding", self.out.getvalue())

        destination = '/root'
        try:
            call_command('exportmd', dest=destination, stdout=self.out, stderr=self.out)
        except PermissionError:
            self.assertRaises(PermissionError)
        self.assertIn('Permisson Error, can not export articles', self.out.getvalue())
