from django.conf.urls import url

from .views import (AllArticles, ArticleDetailView, ArticleListView,
                    ArticleManagementView, CreateArticleView,
                    DeleteArticleView, UpdateArticleView,
                    TaggedArticleListView)

app_name = 'articles'

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='index'),
    url(r'^archives/$', AllArticles.as_view(), name='all'),
    url(r'^archives/(?P<slug>[\-\w]+)/$',
        ArticleDetailView.as_view(),
        name='detail'),
    url(r'tags/(?P<tag>[\-_\w\s]+)/$',
        TaggedArticleListView.as_view(),
        name='tag')
]

# urlpatterns used by backend
urlpatterns += [
    url(r'articles/dashboard/$',
        ArticleManagementView.as_view(),
        name='manage'),
    url(r'^new/articles/$', CreateArticleView.as_view(), name='write'),
    url(r'^edit/articles/(?P<slug>[\-\w]+)/$',
        UpdateArticleView.as_view(),
        name='edit'),
    url(r'delete/articles/(?P<slug>[\-\w]+)/$',
        DeleteArticleView.as_view(),
        name='delete'),
]
