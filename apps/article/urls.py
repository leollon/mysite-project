from django.conf.urls import url

from .views import (AllArticles, ArticleDetailView, ArticleListView,
                    ArticleManagementView, CreateArticleView,
                    DeleteArticleView, UpdateArticleView)

app_name = 'articles'

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='index'),
    url(r'^articles/$', AllArticles.as_view(), name='all'),
    url(r'^articles/(?P<slug>[-\w]+)/detail/$', ArticleDetailView.as_view(),
        name='detail'),
]

# urlpatterns used by backend
urlpatterns += [
    url(r'articles/dashboard/$', ArticleManagementView.as_view(),
        name='manage'),
    url(r'^new/articles/$', CreateArticleView.as_view(), name='write'),
    url(r'^edit/articles/(?P<slug>[-\w]+)/$', UpdateArticleView.as_view(),
        name='edit'),
    url(r'delete/articles/(?P<slug>[-\w]+)/$', DeleteArticleView.as_view(),
        name='delete'),
]
