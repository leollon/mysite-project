from django.contrib.syndication.views import Feed as RSSFeedView
from django.http import JsonResponse
from django.utils.feedgenerator import Atom1Feed

from .article.models import Article
from .core import cache


def online(request):
    online_ips = cache.get('online_ips')
    return JsonResponse({'online_statistics': len(online_ips)})


class RSSArticleFeedView(RSSFeedView):

    title = 'Articles'
    link = '/'
    subtitle = description = 'article list'

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.tags

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return '/'.join(['', 'articles', item.slug])


class AtomArticleFeedView(RSSArticleFeedView):

    feed_type = Atom1Feed
