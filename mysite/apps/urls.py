from django.conf.urls import url

from .article.views import (
    ArticleDetailAPIView, ArticleListAPIView, TaggedArticleListAPIView,
    TagsListAPIView,
)
from .captcha.views import CaptchaAPIView
from .category.views import (
    ArticleCategoryListAPIView, CategorizedArticleListAPIView,
)
from .comment.views import ArticleCommentListAPIView

app_name = 'api'

urlpatterns = [
    url(r"^tags/$", TagsListAPIView.as_view(), name="tag_list"),
    url(r"^refresh/captcha/$", CaptchaAPIView.as_view(), name="captcha"),
    url(r"^articles/$", ArticleListAPIView.as_view(), name="article_list"),
    url(r"^categories/$", ArticleCategoryListAPIView.as_view(), name="category_list"),
    url(r"^articles/(?P<slug>[\-\w]+)/$", ArticleDetailAPIView.as_view(), name="article_detail"),
    url(r"^tags/(?P<tag>[\-\w\ ]+)/articles/$", TaggedArticleListAPIView.as_view(), name="tagged_articles"),
    url(r"^articles/(?P<slug>[\-\w]+)/comments/$", ArticleCommentListAPIView.as_view(), name="article_comment_list"),
    url(
        r"^categories/(?P<name>[\-\w\ ]+)/articles/$",
        CategorizedArticleListAPIView.as_view(),
        name="categorized_articles"),
]
