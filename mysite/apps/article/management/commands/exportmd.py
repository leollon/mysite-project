from pathlib import Path
from datetime import datetime
from functools import wraps

from django.core.management.base import BaseCommand, CommandError

from apps.article.models import Article
from utils.primer import primer_generator


@primer_generator
def export_coroutine():
    while True:
        article, destination = yield
        export_to_markdown(article, destination)


def export_to_markdown(article=None, destination=None):
    datetime_format_string = "%Y-%m-%d %H:%M:%S"
    filename = "%s.md" % article.title
    if not Path(destination).exists():
        Path(destination).mkdir(mode=511)
    with open(str(Path(destination)/filename), 'w') as fp:
        fp.write("---\ntitle: %s\n" % article.title)
        fp.write("date: %s\n" % article.created_time.strftime(
            datetime_format_string))
        fp.write("categories: %s\n" % article.category.name)
        fp.write("tags: [%s]\n---\n\n" % article.tags.split(','))
        fp.write("%s" % article.article_body)

class Command(BaseCommand):
    """Export command for exporting article(s) to markdown file(s)
    """
    help = "export article content to markdown file."
    parent_dir = Path(__file__).parent.parent
    gen = export_coroutine()

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            nargs='?',
            default=None,
            help="Default, export all articles"
        )
        parser.add_argument(
            '-d',
            '--dest',
            nargs='?',
            type=str,
            default="%s" % str(self.parent_dir / 'markdown'),
            help="Default, specify export destination directory"
        )
        parser.add_argument(
            '-p',
            '--post',
            nargs='*',
            action='store',
            type=int,
            help="export an article to a markdown file by an integer."
        )

    def handle(self, *args, **options):
        destination = options.get('dest')
        article_id_list = options.get('post') if options.get('post') else None
        if article_id_list:
            for article_id in article_id_list:
                self.gen.send((Article.objects.get(id=article_id), destination))
        else:
            for article in Article.objects.all():
                self.gen.send((article, destination))
