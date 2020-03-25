from django.urls import re_path

from .article.views import (
    ArticleDetailAPIView, ArticleListAPIView, TaggedArticleListAPIView,
    TagsListAPIView,
)
from .captcha.views import CaptchaAPIView
from .category.views import (
    ArticleCategoryListAPIView, CategorizedArticleListAPIView,
)
from .comment.views import ArticleCommentListAPIView
from .views import online

app_name = 'api'

urlpatterns = [
    re_path(r"^online/$", online),
    re_path(r"^tags/$", TagsListAPIView.as_view(), name="tag_list"),
    re_path(r"^refresh/captcha/$", CaptchaAPIView.as_view(), name="captcha"),
    re_path(r"^articles/$", ArticleListAPIView.as_view(), name="article_list"),
    re_path(r"^categories/$", ArticleCategoryListAPIView.as_view(), name="category_list"),
    re_path(r"^articles/(?P<slug>[\-\w]+)/$", ArticleDetailAPIView.as_view(), name="article_detail"),
    re_path(r"^tags/(?P<tag>[\-\w\ ]+)/articles/$", TaggedArticleListAPIView.as_view(), name="tagged_articles"),
    re_path(r"^articles/(?P<slug>[\-\w]+)/comments/$", ArticleCommentListAPIView.as_view(), name="article_comment_list"),
    re_path(
        r"^categories/(?P<name>[\-\w\ ]+)/articles/$",
        CategorizedArticleListAPIView.as_view(),
        name="categorized_articles"),
]
