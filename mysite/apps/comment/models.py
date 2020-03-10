from django.db import models
from django.urls import reverse

from ..article.models import Article

from apps.core import MyModelBase  # noqa: isort:skip


class Comment(MyModelBase):
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=32, blank=True)
    link = models.URLField(max_length=32, blank=True)
    comment_text = models.TextField(max_length=256)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.comment_text

    def get_absolute_url(self):
        return reverse('api:article_detail', args=(self.post.slug,))

    class Meta:
        ordering = ('created_time',)
        db_table = 'comments'
