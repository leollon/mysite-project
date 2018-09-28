from apps.category.models import ArticleCategory
from apps.users.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Article(models.Model):
    """
    an article model - control the way to access data in the database
    """
    title = models.CharField(max_length=256)
    article_body = models.TextField()
    created_time = models.DateField(auto_now_add=True)
    view_times = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ArticleCategory, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.title

    @staticmethod
    def get_absolute_url():
        return reverse('article:manage')

    class Meta:
        db_table = 'articles'
