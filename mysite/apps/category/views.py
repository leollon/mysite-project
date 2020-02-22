from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from ..article.models import Article
from ..article.serializers import ArticleModelSerializer
from .models import ArticleCategory
from .serializers import ArticleCategoryModelSerializer

from apps.core import CustomizedCursorPagination  # noqa: isort:skip


class ArticleCategoryListAPIView(generics.ListAPIView):

    serializer_class = ArticleCategoryModelSerializer
    http_method_names = ('get', 'options',)
    queryset = ArticleCategory.objects.all()


class CategorizedArticleListAPIView(generics.ListAPIView):

    serializer_class = ArticleModelSerializer
    http_method_names = ('get', 'options', )
    pagination_class = CustomizedCursorPagination
    lookup_field = lookup_url_kwargs = 'name'

    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwargs)
        queryset = Article.objects.filter(Q(category__name=name))
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = super(CategorizedArticleListAPIView, self).list(request, *args, **kwargs)
        article_statistics = ArticleCategory.objects.get(name=self.kwargs.get(self.lookup_field)).article_statistics
        serializer.data['article_statistics'] = article_statistics
        return Response(serializer.data)
