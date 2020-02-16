import re

from django.conf import settings
from django.db import models

from apps.core import MyModelBase  # noqa: isort:skip


class ArticleCategory(MyModelBase):
    """each article category"""

    name = models.CharField(max_length=64, blank=False, unique=True)

    @property
    def article_statistics(self):
        return self.article_set.count()

    @article_statistics.setter
    def article_statistics(self, value):
        raise NotImplementedError

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.filter_data()
        super(ArticleCategory, self).save(*args, **kwargs)

    def filter_data(self):
        self.name = re.sub(settings.CATEGORY_FILTER_PATTERN, '-', self.name)

    class Meta:
        db_table = "categories"
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ('created_time', )
