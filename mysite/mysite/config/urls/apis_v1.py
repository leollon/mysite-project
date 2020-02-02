from django.conf.urls import url

from apps.article.views import ArticleAPIView, TaggedArticleListAPIView, TagsListAPIView  # noqa: isort:skip
from apps.category.views import ArticleCategoryAPIView, CategorizedArticleAPIView  # noqa: isort:skip


urlpatterns = [
    url(r"articles/", ArticleAPIView.as_view()),
    url(r"categories/$", ArticleCategoryAPIView.as_view()),
    url(r"categories/(?P<name>[\-\w\s]+)/$", CategorizedArticleAPIView.as_view()),
    url(r"tags/(?P<tag>[\-\w\s]+)/$", TaggedArticleListAPIView.as_view()),
    url(r"tags/", TagsListAPIView.as_view()),
]
