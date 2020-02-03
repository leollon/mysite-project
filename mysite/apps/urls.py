from django.conf.urls import url

from .article.views import (
    ArticleDetailAPIView, ArticleListAPIView, TaggedArticleListAPIView,
    TagsListAPIView,
)
from .category.views import ArticleCategoryAPIView, CategorizedArticleAPIView

urlpatterns = [
    url(r"articles/(?P<slug>[\-\w]+)/$", ArticleDetailAPIView.as_view()),
    url(r"tags/(?P<tag>[\-\w\ ]+)/$", TaggedArticleListAPIView.as_view()),
    url(r"categories/(?P<name>[\-\w\ ]+)/$", CategorizedArticleAPIView.as_view()),
    url(r"tags/", TagsListAPIView.as_view()),
    url(r"articles/", ArticleListAPIView.as_view()),
    url(r"categories/$", ArticleCategoryAPIView.as_view()),
]
