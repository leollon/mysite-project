from django.contrib import sitemaps

from apps.article.models import Article  # noqa: isort:skip


class ArticleSiteMap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.3
    protocol = "https"

    def items(self):
        return Article.objects.all()

    def lastmod(self, item):
        return item.created_time

    def location(self, item):
        return item.get_absolute_url()
