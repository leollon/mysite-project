from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic import ListView
from rest_framework import generics

from ..article.models import Article
from ..article.serializers import ArticleModelSerializer
from .models import ArticleCategory
from .serializers import ArticleCategoryModelSerializer

from apps.core import CustomizedCursorPagination  # noqa: isort:skip

per_page = settings.PER_PAGE


class CategoryListView(ListView):
    """Get all categories"""
    model = ArticleCategory
    template_name = 'category/all_categories.html'
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        return super(CategoryListView, self).get(request, *args, **kwargs)


class CategorizeArticleListView(ListView):
    """Get all articles based on category name"""
    model = Article
    context_object_name = 'articles'
    paginate_by = per_page
    template_name = 'article/index.html'

    def get_queryset(self):
        name = self.kwargs.get('name', 'uncategoriezed')
        try:
            category = ArticleCategory.objects.get(name=name)
        except ArticleCategory.DoesNotExist:
            raise Http404(_(repr(name) + " not found"))
        else:
            return super(CategorizeArticleListView, self).get_queryset().filter(category=category)

    def get_context_data(self, **kwargs):
        context = dict()
        context['category'] = ArticleCategory.objects.get(
            name=self.kwargs.get('name', 'uncategorized'))
        return super(CategorizeArticleListView, self).get_context_data(**context)


class ArticleCategoryAPIView(generics.ListAPIView):

    serializer_class = ArticleCategoryModelSerializer
    http_method_names = ('get', 'options',)
    queryset = ArticleCategory.objects.all()


class CategorizedArticleAPIView(generics.ListAPIView):

    serializer_class = ArticleModelSerializer
    http_method_names = ('get', 'options', )
    pagination_class = CustomizedCursorPagination
    lookup_field = lookup_url_kwargs = 'name'

    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwargs)
        queryset = Article.objects.filter(Q(category__name=name))
        return queryset
