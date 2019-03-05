import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ArticleCategory(models.Model):
    """each article category"""

    name = models.CharField(max_length=64, blank=False, unique=True)
    created_time = models.DateTimeField(null=True, auto_now_add=True)

    def count_number(self):
        return self.article_set.count()

    count_number.short_description = 'article number'

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.filter_data()
        super(ArticleCategory, self).save(*args, **kwargs)

    def filter_data(self):
        pat = re.compile(r'[^\-\w\s]+')
        self.name = re.sub(pat, '', self.name)

    class Meta:
        db_table = "categories"
        verbose_name = "category"
        verbose_name_plural = "categories"
