from collections import Counter, OrderedDict

from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.base import View
from ipware.ip import get_real_ip
from rest_framework import generics
from utils import cache

from .models import Article
from .serializers import ArticleModelSerializer
from .tasks import increment_page_view_times, increment_user_view_times

from apps.core import CustomizedCursorPagination  # noqa: isort:skip


class BaseArticleAPI(generics.ListAPIView):

    serializer_class = ArticleModelSerializer
    pagination_class = CustomizedCursorPagination
    http_method_names = ('get', 'options', )


class ArticleListAPIView(BaseArticleAPI):

    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ArticleDetailAPIView(generics.RetrieveAPIView):

    serializer_class = ArticleModelSerializer
    lookup_field = lookup_url_kwargs = 'slug'
    queryset = Article.objects.all()
    http_method_names = ("get", "options", )

    def get(self, request, *args, **kwargs):
        day = 0
        self.object = super(ArticleDetailAPIView, self).get_object()
        ip = get_real_ip(request)
        visited_ips = cache.get(self.object.slug, set())

        if ip not in visited_ips:
            visited_ips.add(ip)
            cache.set(self.object.slug, visited_ips, day)
            increment_user_view_times.delay(article_id=self.object.id)
        increment_page_view_times.delay(article_id=self.object.id)
        return self.retrieve(request, *args, **kwargs)


class TaggedArticleListAPIView(BaseArticleAPI):
    """Get all article belonging to a specified tag
    """

    lookup_field = lookup_url_kwargs = 'tag'

    def get_queryset(self):

        queryset = Article.objects.filter(Q(tags__icontains=self.kwargs.get(self.lookup_url_kwargs)))
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TagsListAPIView(View):
    """Get all tags"""

    http_method_names = ('get', 'options', )

    def get(self, request, *args, **kwargs):

        tags_str_list = Article.objects.values_list('tags', flat=True)
        tags_counter = Counter()
        for tag_str in tags_str_list:
            tags_counter.update(tag_str.lower().split(','))
        return JsonResponse(
            OrderedDict([('tags', tags_counter), ('count', len(tags_counter.keys())), ]))
