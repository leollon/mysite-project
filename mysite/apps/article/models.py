import uuid

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from ..category.models import ArticleCategory
from ..user.models import User
from .mixins import ArticleCleanedMixin


def default_slug():
    return str(uuid.uuid4())


class Article(models.Model, ArticleCleanedMixin):
    """
    an article model - control the way to access data in the database
    """

    title = models.CharField(max_length=256)
    article_body = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
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

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.clean_data()
        super(Article, self).save(*args, **kwargs)

    @staticmethod
    def get_absolute_url():
        return reverse("article:manage")

    class Meta:
        ordering = ("-created_time",)
        db_table = "articles"
