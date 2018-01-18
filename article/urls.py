from django.conf.urls import url
from article import views

app_name = 'article'

urlpatterns = [
    url(r'^$', views.ArticleListView.as_view(), name='index'),
    url(r'^all/$', views.AllArticles.as_view(), name='all'),
    url(r'^post/new/$', views.CreateArticleView.as_view(), name='write'),
    url(r'^post/(?P<pk>[\d]+)/$', views.ArticleDetailView.as_view(),
        name='detail'),
    url(r'^post/edit/(?P<pk>[\d]+)/$', views.UpdateArticleView.as_view(),
        name='edit'),
]

# urlpatterns used by backend
urlpatterns += [
    url(r'post/management/', views.ArticleManagementView.as_view(),
        name='manage'),
    url(r'post/(?P<pk>[\d]+)/delete/$', views.DeleteArticleView.as_view(),
        name='delete'),
]