from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from apps.article.models import Article


@python_2_unicode_compatible
class Comment(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=32, blank=True)
    link = models.URLField(max_length=32, blank=True)
    comment_text = models.TextField(max_length=256)
    created_time = models.DateTimeField(auto_now=True, null=True)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.comment_text

    class Meta:
        ordering = ("created_time", )
        db_table = "comments"