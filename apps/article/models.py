import uuid
import unicodedata 

from django.utils.text import slugify
from django.db import models
from django.shortcuts import reverse

from unidecode import unidecode
from apps.category.models import ArticleCategory
from apps.users.models import User


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
        max_length=100, null=True,
        unique=True, default=default_slug
        )
    view_times = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ArticleCategory, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tags = models.CharField(
        max_length=32, default="untagged",
        blank=True, help_text="使用逗号分隔")

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        if not self.tags: self.tags = "untagged"
        super(Article, self).save(*args, **kwargs)

    @staticmethod
    def get_absolute_url():
        return reverse('articles:manage')

    class Meta:
        db_table = 'articles'
