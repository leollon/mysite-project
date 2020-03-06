import re
from datetime import datetime
from pathlib import Path
from typing import Generator, Iterator

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DataError, IntegrityError
from django.utils.text import slugify
from unidecode import unidecode
from utils import primer_generator

from ....article.models import Article
from .constants import Importation

from apps.category.models import ArticleCategory  # noqa: isort:skip
from apps.user.models import User  # noqa: isort:skip


try:
    author = User.objects.get(pk=1)
except User.DoesNotExist:
    author = User.objects.create_superuser(**settings.IMPORT_ARTICLE_USER, is_valid=True)


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

        try:
            file_list = list(Path(options['dir']).iterdir())
        except FileNotFoundError:
            raise CommandError(self.parent_dir.joinpath(options['dir']).as_posix() + " directory does not exist.")
        else:
            if not file_list:
                raise CommandError(
                    "please specify a directory containing markdown files")
        path = Path(options['dir']).glob('**/*')

        group = self.grouper()
        for file in path:
            if file.is_file():
                group.send(file.as_posix())
        group.send(None)
        settings.USE_TZ = True
        self.stdout.close()

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
        if filepath is None:
            return

        message, flag = '', ''
        slug = slugify(unidecode(filepath.split('/')[-1].split('.')[0]))
        article_body, title = '', slug
        category_name, tags, date = 'uncategorized', 'untagged', datetime.now()
        category, _ = ArticleCategory.objects.get_or_create(name=category_name)

        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                if not line.startswith('---'):
                    if line.startswith('title'):
                        title = re.search(settings.TITLE_PATTERN, line).group(1)
                    elif line.startswith('date'):
                        date = datetime.strptime(
                            re.search(settings.DATETIME_PATTERN, line).group(1), settings.DATETIME_FORMAT_STRING)
                    elif line.startswith('categories') or line.startswith('category'):
                        result = re.search(settings.CATEGORY_PATTERN, line)
                        if result:
                            category, _ = ArticleCategory.objects.get_or_create(
                                name=re.sub(settings.CATEGORY_FILTER_PATTERN, '-', result.group(1)))
                    elif line.startswith('tags'):
                        tags = re.search(settings.TAGS_ARRAY_PATTERN, line).group(1)
                        tags = re.sub(settings.TAGS_WHITESPACE_PATTERN, ',', tags)
                        tags = re.sub(settings.TAGS_FILTER_PATTERN, '', tags).strip(',')
                    else:
                        article_body += line

            try:
                Article.objects.create(
                    title=title, article_body=article_body,
                    category=category, author=author,
                    tags=tags, slug=slug,
                    created_time=date)
                message = self._success("Finish importing %s." % repr(filepath))
                flag = Importation.DONE
            except IntegrityError as e:
                message = self._warning(
                    "Article %s already exists. message: %s" % (repr(title), e))
                flag = Importation.REPLICA
            except DataError as e:
                message = self._error(
                    "Import %s Error, msessage: %s." % (repr(filepath), e))
                flag = Importation.ERROR
            self.output_results(flag, message)

    def output_results(self, flag: Importation, message: str) -> None:
        if flag in (Importation.REPLICA, Importation.DONE):
            self.stdout.write(message)
        elif flag == Importation.ERROR.value:
            self.stderr.write(message)
        self.stdout.flush()
