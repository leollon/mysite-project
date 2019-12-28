import sys
from pathlib import Path
from typing import Generator, Tuple

from django.core.management.base import BaseCommand
from utils import primer_generator

from .constans import Exportation

from apps.article.models import Article  # noqa: isort:skip


class Command(BaseCommand):
    """Export command for exporting article(s) to markdown file(s)
    """

    help = "export article content to markdown file."
    parent_dir = Path(__file__).parent.parent

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(force_color=True, *args, **kwargs)
        self._success = self.style.SUCCESS
        self._error = self.style.ERROR

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-a",
            "--all",
            nargs="?",
            default=None,
            help="Default, export all articles",)
        parser.add_argument(
            "-d",
            "--dest",
            nargs="?",
            type=str,
            default=(self.parent_dir / "markdown").as_posix(),
            help="Default, specify export destination directory",)
        parser.add_argument(
            "-p",
            "--post",
            nargs="*",
            action="store",
            type=int,
            help="export an article to a markdown file by an integer.",)

    def handle(self, *args, **options) -> None:
        destination = options.get("dest")
        gen = self.export_coroutine()
        article_id_list = []
        if options.get("post"):
            article_id_list = options.get("post")
        if article_id_list:
            for article_id in article_id_list:
                try:
                    article = Article.objects.get(id=article_id)
                except Article.DoesNotExist:
                    self.output_result(
                        Exportation.ERROR,
                        self._error("Not exists the article corresponding to this id: %d.\n" % article_id))
                else:
                    gen.send((article, destination))
        else:
            for article in Article.objects.all():
                gen.send((article, destination))
        sys.stdout.close()

    @primer_generator
    def export_coroutine(self) -> Generator[None, Tuple, None]:
        while True:
            article, destination = yield
            self.export_to_markdown(article, destination)

    def export_to_markdown(self, article: Article, destination: str) -> None:
        datetime_format_string = "%Y-%m-%d %H:%M:%S"
        filename = "".join([article.slug, ".md"])
        try:
            Path(destination).mkdir(mode=0o755, exist_ok=True)
            with open((Path(destination) / filename).as_posix(), "w") as fp:
                content = (
                    "---\ntitle: %s\ndate: %s\ncategories: %s\ntags: %s\n---\n\n%s"
                    % (
                        article.title,
                        article.created_time.strftime(datetime_format_string),
                        article.category.name,
                        article.tags.split(","),
                        article.article_body,
                    )
                )
                fp.write(content)
            message = self._success("Exported %s.\n" % repr(article.title))
            flag = Exportation.DONE
        except PermissionError as e:
            message = self._error("Permisson Error, can export articles.\n%s\n" % e)
            flag = Exportation.ERROR
        self.output_result(flag, message)

    def output_result(self, flag, message):
        if flag in (Exportation.DONE, Exportation.EXISTENTCE):
            sys.stdout.write(message)
        elif flag == Exportation.ERROR:
            sys.stderr.write(message)
        sys.stdout.flush()
