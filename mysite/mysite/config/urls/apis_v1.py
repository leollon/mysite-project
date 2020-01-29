from django.conf.urls import url

from apps.article.views import ArticleAPIView  # noqa isort:skip

urlpatterns = [
    url("articles/", ArticleAPIView.as_view()),
]
