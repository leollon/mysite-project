import re

from django.conf import settings
from django.db import models

from apps.core import MyModelBase  # noqa: isort:skip


class ArticleCategory(MyModelBase):
    """each article category"""

    name = models.CharField(max_length=64, blank=False, unique=True)

    def count_number(self):
        return self.article_set.count()

    count_number.short_description = 'article number'

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
