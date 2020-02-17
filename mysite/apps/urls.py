from django.conf.urls import url

from .article.views import (
    ArticleDetailAPIView, ArticleListAPIView, TaggedArticleListAPIView,
    TagsListAPIView,
)
from .category.views import ArticleCategoryAPIView, CategorizedArticleAPIView
from .comment.views import CommentListAPIView

app_name = 'api'

urlpatterns = [
    url(r"articles/(?P<slug>[\-\w]+)/$", ArticleDetailAPIView.as_view(), name="article_detail"),
    url(r"tags/(?P<tag>[\-\w\ ]+)/$", TaggedArticleListAPIView.as_view(), name="tagged_articles"),
    url(r"categories/(?P<name>[\-\w\ ]+)/$", CategorizedArticleAPIView.as_view(), name="categorized_articles"),
    url(r"tags/$", TagsListAPIView.as_view(), name="tag_list"),
    url(r"articles/$", ArticleListAPIView.as_view(), name="article_list"),
    url(r"categories/$", ArticleCategoryAPIView.as_view(), name="category_list"),
    url(r"articles/(?P<slug>[\-\w]+)/comments/$", CommentListAPIView.as_view(), name="article_comment_list"),
]
