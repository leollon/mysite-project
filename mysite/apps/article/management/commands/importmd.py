import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Generator, Iterator

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DataError, IntegrityError

from utils import primer_generator

from .constans import Importation

from apps.article.models import Article  # noqa: isort:skip
from apps.category.models import ArticleCategory  # noqa: isort:skip
from apps.user.models import User  # noqa: isort:skip


try:
    author = User.objects.get(pk=1)
except User.DoesNotExist:
    author = User.objects.create_user(**settings.IMPORT_ARTICLE_USER)


class Command(BaseCommand):
    """Customized command for importing content from markdown.
    """
    help = "import article content from markdown file."
    parent_dir = Path(__file__).parent.parent
    results = {}

    def __init__(self, *args, **kwargs):
        super().__init__(force_color=True, *args, **kwargs)
        self._warning = self.style.WARNING
        self._success = self.style.SUCCESS
        self._error = self.style.ERROR

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--dir',
            nargs="?",
            type=str,
            default=str(self.parent_dir / 'markdown'),
            help="default: %s." % str(self.parent_dir / 'markdown')
        )

    def handle(self, *args, **options) -> None:
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
        sys.stdout.close()

    def line_handler(self, line) -> str:
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
    def grouper(self) -> Generator:
        while True:
            yield from self.read_from_md()

    def read_from_md(self) -> Iterator:
        """
        Read content from markdown file into article model,
        save the content in PostgreSQL.
        """
        filepath = yield
        article_body, title, tags, date = '', '', '', datetime.now()
        message, flag = '', ''

        if filepath is None:
            return
        slug = filepath.split('/')[-1].split('.')[0]
        category, _ = ArticleCategory.objects.get_or_create(name="uncategorized")
        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                if not line.startswith('---'):
                    if line.startswith('title'):
                        title = self.line_handler(line)
                    elif line.startswith('date'):
                        date = datetime.strptime(
                            self.line_handler(line), settings.DATETIME_FORMAT_STRING)
                    elif line.startswith('categories'):
                        name = self.line_handler(line).strip("'")
                        name = re.sub(settings.NAME_PATTERN, '', name)
                        category, _ = ArticleCategory.objects.get_or_create(name=name)
                    elif line.startswith('tags'):
                        tags_string = re.sub(
                            settings.TAGS_ARRAY_PATTERN, '', self.line_handler(line))
                        tags_string = re.sub(
                            settings.TAGS_WHITESPACE_PATTERN, ',', tags_string)
                        tags = re.sub(
                            settings.TAGS_FILTER_PATTERN, '', tags_string).strip(',')
                    else:
                        article_body += line

            try:
                Article.objects.create(
                    title=title,
                    article_body=article_body,
                    category=category,
                    author=author,
                    tags=tags,
                    slug=slug,
                    created_time=date)
                message = self._success(
                    "Finish importing %s." % repr(filepath))
                flag = Importation.DONE
            except IntegrityError as e:
                message = self._warning(
                    "Article %s exists. message: %s" % (repr(title), e))
                flag = Importation.REPLICA
            except DataError as e:
                message = self._error(
                    "Import %s Error, msessage: %s." % (repr(filepath), e))
                flag = Importation.ERROR
                self.output_results(flag, message)
            self.output_results(flag, message)

    def output_results(self, flag: Importation, message: str) -> None:
        if flag in (Importation.REPLICA, Importation.DONE):
            self.stdout.write(message)
        elif flag == Importation.ERROR.value:
            self.stderr.write(message)
        sys.stdout.flush()
