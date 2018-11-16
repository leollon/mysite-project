from django.contrib import sitemaps
from django.urls import reverse

from apps.article.models import Article


class ArticleSiteMap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.3
    protocol = "https"

    def items(self):
        return Article.objects.all()

    def lastmod(self, item):
        return item.created_time

    def location(self, item):
        return reverse("articles:detail", args=(item.slug, ))
