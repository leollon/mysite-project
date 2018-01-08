from django.db import models
from django.utils.encoding import python_2_unicode_compatible


from article.models import Article


@python_2_unicode_compatible
class Comment(models.Model):
    username = models.CharField(max_length=32, blank=False)
    email = models.EmailField(max_length=32, blank=True)
    link = models.CharField(max_length=32, blank=True)
    comment_text = models.TextField(max_length=256, blank=False)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.comment_text
