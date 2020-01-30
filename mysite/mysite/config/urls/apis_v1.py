from django.conf.urls import url

from apps.article.views import ArticleAPIView  # noqa: isort:skip
from apps.category.views import ArticleCategoryAPIView, CategorizedArticleAPIView  # noqa: isort:skip


urlpatterns = [
    url(r"articles/", ArticleAPIView.as_view()),
    url(r"categories/$", ArticleCategoryAPIView.as_view()),
    url(r"categories/(?P<name>[\-\w\s]+)/$", CategorizedArticleAPIView.as_view())
]
