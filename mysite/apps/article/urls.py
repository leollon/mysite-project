from django.conf.urls import url

from .apis_v1 import ArticleAPIView
from .views import (
    ArticleDetailView, ArticleListView, ArticleManagementView,
    CreateArticleView, DeleteArticleView, IndexView, TaggedArticleListView,
    UpdateArticleView,
)

app_name = "article"

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^articles/$", ArticleAPIView.as_view()),
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

# urlpatterns used by backend
urlpatterns += [
    url(
        r"articles/dashboard/$", ArticleManagementView.as_view(), name="manage"
    ),
    url(r"^new/articles/$", CreateArticleView.as_view(), name="write"),
    url(
        r"^edit/articles/(?P<slug>[\-\w]+)/$",
        UpdateArticleView.as_view(),
        name="edit",
    ),
    url(
        r"delete/articles/(?P<slug>[\-\w]+)/$",
        DeleteArticleView.as_view(),
        name="delete",
    ),
]
