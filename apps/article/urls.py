from django.conf.urls import url
from .views import (ArticleList, AllArticles, CreateArticleView,
                    ArticleDetailView, UpdateArticleView,
                    ArticleManagementView, DeleteArticleView
                    )

app_name = 'article'

urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='index'),
    url(r'^all/$', AllArticles.as_view(), name='all'),
    url(r'^post/new/$', CreateArticleView.as_view(), name='write'),
    url(r'^post/(?P<pk>[\d]+)/$', ArticleDetailView.as_view(),
        name='detail'),
    url(r'^post/edit/(?P<pk>[\d]+)/$', UpdateArticleView.as_view(),
        name='edit'),
]

# urlpatterns used by backend
urlpatterns += [
    url(r'post/management/', ArticleManagementView.as_view(),
        name='manage'),
    url(r'post/(?P<pk>[\d]+)/delete/$', DeleteArticleView.as_view(),
        name='delete'),
]