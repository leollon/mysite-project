from django.db import models
from django.shortcuts import reverse


class Article(models.Model):
    """
        an article model
    """
    title = models.CharField(max_length=256)
    article_summary = models.TextField()
    article_body = models.TextField()
    created_time = models.DateField(auto_now=True)
    view_times = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.title

    def __unicode__(self):
        return "%s" % self.title

    @staticmethod
    def get_absolute_url():
        return reverse('article:index')
