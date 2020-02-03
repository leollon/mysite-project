from django.conf.urls import url

from .views import (
    ArticleDetailView, ArticleListView, IndexView, TaggedArticleListView,
)

app_name = "article"

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^archives/$", ArticleListView.as_view(), name="all"),
    url(
        r"^archives/(?P<slug>[\-\w]+)/$",
        ArticleDetailView.as_view(),
        name="detail",
    ),
    url(
        r"tag/(?P<tag>[\-\w\s]+)/$", TaggedArticleListView.as_view(), name="tag"
    ),
]
