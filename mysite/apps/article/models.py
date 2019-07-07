import re
import uuid
import unicodedata

from django.utils.text import slugify
from django.db import models
from django.shortcuts import reverse
from django.conf import settings

from unidecode import unidecode
from apps.category.models import ArticleCategory
from apps.user.models import User


def default_slug():
    return str(uuid.uuid4())


class Article(models.Model):
    """
    an article model - control the way to access data in the database
    """

    title = models.CharField(max_length=256)
    article_body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=100, null=True, unique=True, default=default_slug
    )
    view_times = models.PositiveIntegerField(default=0)
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

    def clean_data(self):
        self.slug = slugify(unidecode(self.title))
        if not self.tags:
            self.tags = "untagged"
        else:
            self.tags = re.sub(
                settings.TAGS_FILTER_PATTERN, "", self.tags
            ).strip(",")

    @staticmethod
    def get_absolute_url():
        return reverse("article:manage")

    class Meta:
        ordering = ("-created_time",)
        db_table = "articles"
