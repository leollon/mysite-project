from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ArticleCategory(models.Model):
    """each article category"""

    class META:
        db_table = "article_category"

    name = models.CharField(max_length=64)

    def count_number(self):
        return self.article_set.count()

    count_number.short_description = 'article number'

    def __str__(self):
        return '%s' % self.name
