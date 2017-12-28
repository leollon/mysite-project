from django.conf.urls import url
from article import views

app_name = 'article'

urlpatterns = [
    url(r'^$', views.ArticleList.as_view(), name='index'),
    url(r'^all/$', views.AllArticles.as_view(), name='all'),
    url(r'^write/$', views.CreateArticleView.as_view(), name='write'),
    url(r'^post/(?P<pk>[\d]+)/$', views.ArticleDetailView.as_view(),
        name='detail'),
    url(r'^post/(?P<pk>[\d]+)/edit/$', views.UpdateArticleView.as_view(),
        name='edit'),
]

# urlpatterns used by backend
urlpatterns += [
    url(r'article/management/', views.ArticleManagement.as_view(),
        name='manage'),
]