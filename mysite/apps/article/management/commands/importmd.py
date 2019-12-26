import re
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DataError, IntegrityError

from apps.article.models import Article
from apps.category.models import ArticleCategory
from apps.user.models import User
from utils.primer import primer_generator

IMPORTED = 0
REPLICA = 1
ERROR = 2

try:
    author = User.objects.get(pk=1)
except User.DoesNotExist:
    author = User.objects.create_user(**getattr(settings, 'IMPORT_ARTICLE_USER'))


class Command(BaseCommand):
    """Customized command for importing content from markdown.
    """
    help = "import article content from markdown file."
    parent_dir = Path(__file__).parent.parent
    results = {}

    def __init__(self, *args, **kwargs):
        super().__init__(force_color=True, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--dir',
            nargs="?",
            type=str,
            default=str(self.parent_dir / 'markdown'),
            help="default: %s." % str(self.parent_dir / 'markdown')
        )

    def handle(self, *args, **options):
        settings.USE_TZ = False
        if not list(Path(options['dir']).iterdir()):
            raise CommandError(
                "please specify a directory containing markdown files")
        path = Path(options['dir']).glob('**/*')

        group = self.grouper()
        for file in path:
            if file.is_file():
                group.send(file.as_posix())
        group.send(None)
        settings.USE_TZ = True

    def line_handler(self, line):
        """
        Examples

            >>> line = 'tags: [1, 2, 3]'
            >>> Command().line_handler(line)
            '1, 2, 3'

            >>> line = 'title: hello-world'
            >>> Command().line_handler(line)
            'hello-world'
        """
        ret_val = line.partition(':')[-1].strip()
        return ret_val

    @primer_generator
    def grouper(self):
        while True:
            yield from self.read_from_md()

    def read_from_md(self):
        """
        Read content from markdown file into article model,
        save the content in MySQL.
        """
        filepath = yield
        article_body, tags = '', ''
        date = datetime.now()
        message, flag = '', ''

        if filepath is None:
            return
        title = re.sub(settings.TITLE_PATTERN, '-', filepath.split('/')[-1].split('.')[0])
        try:
            category = ArticleCategory.objects.get(pk=1)
        except ArticleCategory.DoesNotExist:
            category = ArticleCategory.objects.create(name="uncategorized")
        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                if not line.startswith('---'):
                    if line.startswith('title'):
                        continue
                    elif line.startswith('date'):
                        date = datetime.strptime(
                            self.line_handler(line), settings.DATETIME_FORMAT_STRING)
                    elif line.startswith('categories'):
                        name = self.line_handler(line).strip("'")
                        name = re.sub(settings.NAME_PATTERN, '', name)
                        try:
                            category = ArticleCategory.objects.get(name=name)
                        except ArticleCategory.DoesNotExist:
                            category = ArticleCategory(name=name)
                            category.save()
                    elif line.startswith('tags'):
                        tags_string = re.sub(
                            settings.TAGS_ARRAY_PATTERN, '', self.line_handler(line)
                        )
                        tags_string = re.sub(
                            settings.TAGS_WHITESPACE_PATTERN, ',', tags_string
                        )
                        tags = re.sub(
                            settings.TAGS_FILTER_PATTERN, '', tags_string
                        ).strip(',')
                    else:
                        article_body += line

            try:
                article = Article.objects.create(
                    title=title,
                    article_body=article_body,
                    category=category,
                    author=author,
                    tags=tags)
                article.created_time = date
                article.save()
                message, flag = self.style.SUCCESS("Finish importing %s." % repr(filepath)), IMPORTED
            except IntegrityError as e:
                message, flag = self.style.WARNING("Article %s exists. message: %s" % (repr(title), e)), REPLICA
            except DataError as e:
                message, flag = self.style.ERROR("Import %s Error, msessage: %s." % (repr(filepath), e)), ERROR
                self.output_results(ERROR, message)
            self.output_results(flag, message)

    def output_results(self, flag, message):
        if flag == REPLICA:
            self.stdout.write(message)
        elif flag == IMPORTED:
            self.stdout.write(message)
        elif flag == ERROR:
            self.stderr.write(message)
