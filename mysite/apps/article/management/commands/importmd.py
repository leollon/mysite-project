import re
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import DataError, IntegrityError
from django.conf import settings

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


def line_handler(line):
    """
    Examples

        >>> line = 'tags: [1, 2, 3]'
        >>> line_handler(line)
        '1, 2, 3'

        >>> line = 'title: hello-world'
        >>> line_handler(line)
        'hello-world'
    """
    ret_val = line.partition(':')[-1].strip()
    return ret_val


@primer_generator
def grouper(results):
    index = 0
    while True:
        ret_tuple = yield from read_from_md()
        if None not in ret_tuple:
            results[index] = ret_tuple
        index += 1


def read_from_md():
    """
    Read content from markdown file into article model,
    save the content in MySQL.
    """
    filepath = yield
    article_body = ''
    tags = ''
    date = datetime.now()
    if filepath is None:
        return (None, None, None)
    title = re.sub(settings.TITLE_PATTERN, '-', filepath.split('/')[-1].split('.')[0])
    try:
        category = ArticleCategory.objects.get(pk=1)
    except ArticleCategory.DoesNotExist:
        category = ArticleCategory.objects.create(name="uncategorized")
    with open(filepath, 'r+') as fp:
        for line in fp.readlines():
            if not line.startswith('---'):
                if line.startswith('title'):
                    continue
                elif line.startswith('date'):
                    date = datetime.strptime(
                        line_handler(line), settings.DATETIME_FORMAT_STRING)
                elif line.startswith('categories'):
                    name = line_handler(line).strip("'")
                    name = re.sub(settings.NAME_PATTERN, '', name)
                    try:
                        category = ArticleCategory.objects.get(name=name)
                    except ArticleCategory.DoesNotExist:
                        category = ArticleCategory(name=name)
                        category.save()
                elif line.startswith('tags'):
                    tags_string = re.sub(
                        settings.TAGS_ARRAY_PATTERN, '', line_handler(line)
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
            return (IMPORTED, repr(filepath), 'Imported')
        except IntegrityError as e:
            return (REPLICA, repr(title), e.args[1])
        except DataError as e:
            return (ERROR, repr(filepath), e.args[1])


class Command(BaseCommand):
    """Customized command for importing content from markdown.
    """
    help = "import article content from markdown file."
    parent_dir = Path(__file__).parent.parent
    results = {}

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--dir',
            nargs="?",
            type=str,
            default=str(self.parent_dir / 'markdown'),
            help="default: %s." % str(self.parent_dir / 'markdown'))

    def handle(self, *args, **options):
        settings.USE_TZ = False
        if not list(Path(options['dir']).iterdir()):
            raise CommandError(
                "please specify an directory including markdown files")
        path = Path(options['dir']).glob('**/*')

        group = grouper(self.results)
        for file in path:
            if file.is_file():
                group.send(str(file))
        group.send(None)
        settings.USE_TZ = True
        self.output_results()

    def output_results(self):
        for _, values in self.results.items():
            if values[0] == REPLICA:
                message = "Article %s exists. message: %s" % (values[1], values[2])
                self.stdout.write(self.style.WARNING(message))
            elif values[0] == IMPORTED:
                message = "Finish importing %s." % values[1]
                self.stdout.write(self.style.SUCCESS(message))
            else:
                message = "Import %s Error, msessage: %s." % (values[1], values[2])
                self.stderr.write(self.style.ERROR(message))
