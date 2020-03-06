import uuid

from django.db import models
from django.shortcuts import reverse

from ..category.models import ArticleCategory
from ..user.models import User
from .mixins import ArticleCleanedMixins

from apps.core import MyModelBase  # noqa: isort:skip


def default_slug():
    return str(uuid.uuid4())


class Article(ArticleCleanedMixins, MyModelBase):
    """
    an article model - control the way to access data in the database
    """

    title = models.CharField(max_length=256)
    article_body = models.TextField()
    slug = models.SlugField(
        max_length=100, unique=True, default=default_slug
    )
    user_view_times = models.PositiveIntegerField(default=0)
    page_view_times = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        ArticleCategory, null=True, on_delete=models.SET_NULL
    )
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tags = models.CharField(
        max_length=64, default="untagged", blank=True, help_text="使用逗号分隔"
    )

    @property
    def comment_statistics(self):
        return self.comment_set.count()

    @comment_statistics.setter
    def comment_statistics(self, value):
        raise NotImplementedError

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.clean_data()
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("api:article_detail", args=(self.slug,))

    class Meta:
        ordering = ("-created_time",)
        db_table = "articles"
