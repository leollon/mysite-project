from collections import Counter, OrderedDict

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import BaseCreateView
from ipware.ip import get_real_ip
from rest_framework import generics
from utils import cache

from .models import Article
from .serializers import ArticleModelSerializer
from .tasks import increment_page_view_times, increment_user_view_times

from apps.core import CustomizedCursorPagination  # noqa: isort:skip
from apps.comment.forms import CommentForm  # noqa: isort:skip
from apps.comment.models import Comment  # noqa: isort:skip

PER_PAGE = settings.PER_PAGE


class BaseArticleAPI(generics.ListAPIView):

    serializer_class = ArticleModelSerializer
    pagination_class = CustomizedCursorPagination
    http_method_names = ('get', 'options', )


class IndexView(ListView):
    """Index homepage
    """

    template_name = "article/index.html"
    model = Article
    paginate_by = PER_PAGE
    context_object_name = "articles"

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)


class ArticleListView(ListView):
    template_name = "article/all_articles.html"
    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get(self, request, *args, **kwargs):
        return super(ArticleListView, self).get(request, *args, **kwargs)


class ArticleDetailView(DetailView, BaseCreateView):
    """The detail of each article
    """

    model = Article
    form_class = CommentForm
    template_name = "article/article_detail.html"
    context_object_name = "article"

    def get(self, request, *args, **kwargs):
        day = 0
        self.object = super(ArticleDetailView, self).get_object()
        ip = get_real_ip(request)
        visited_ips = cache.get(self.object.slug, set())

        if ip not in visited_ips:
            visited_ips.add(ip)
            cache.set(self.object.slug, visited_ips, day)
            increment_user_view_times.delay(article_id=self.object.id)
        increment_page_view_times.delay(article_id=self.object.id)
        context = self.get_context_data(object=self.object)
        comments = self.get_comment_list(request, *args, **kwargs)
        context.update({"comments": comments})
        return super(ArticleDetailView, self).render_to_response(context)

    def get_comment_list(self, request, *args, **kwargs):
        comments_list = Comment.objects.filter(post=self.object)
        paginator = Paginator(comments_list, per_page=PER_PAGE, orphans=1)
        comments = paginator.get_page(request.GET.get("page", 1))
        return comments


class TaggedArticleListView(ListView):
    template_name = "article/index.html"
    context_object_name = "articles"
    paginate_by = PER_PAGE
    context_object_name = "articles"

    def get_queryset(self, **kwargs):
        queryset = Article.objects.filter(
            tags__icontains=self.kwargs.get("tag"))
        return queryset

    def get(self, request, *args, **kwargs):
        return super(TaggedArticleListView, self).get(request, *args, **kwargs)


class ArticleListAPIView(BaseArticleAPI):

    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ArticleDetailAPIView(generics.RetrieveAPIView):

    serializer_class = ArticleModelSerializer
    lookup_field = lookup_url_kwargs = 'slug'
    queryset = Article.objects.all()

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
            tags_counter.update(tag_str.split(','))
        return JsonResponse(OrderedDict([('tags', tags_counter), ('count', len(tags_counter.keys())), ]))
