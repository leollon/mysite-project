from django.conf.urls import url

from .views import (AllArticles, ArticleDetailView, ArticleListView,
                    ArticleManagementView, CreateArticleView,
                    DeleteArticleView, UpdateArticleView)

app_name = 'article'

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='index'),
    url(r'^all/$', AllArticles.as_view(), name='all'),
    url(r'^new/article/$', CreateArticleView.as_view(), name='write'),
    url(r'^detail/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(),
        name='detail'),
    url(r'^/edit/article/(?P<slug>[-\w]+)/$', UpdateArticleView.as_view(),
        name='edit'),
]

# urlpatterns used by backend
urlpatterns += [
    url(r'articles/management/', ArticleManagementView.as_view(),
        name='manage'),
    url(r'delete/article/(?P<slug>[-\w]+)/$', DeleteArticleView.as_view(),
        name='delete'),
]
