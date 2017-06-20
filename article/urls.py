from django.conf.urls import url
from article import views

app_name = 'article'

urlpatterns = [
    url(r'^$', views.ArticleList.as_view(), name='index'),
    url(r'^posts/(?P<pk>[\d]+)/$', views.ArticleDetail.as_view(), name='detail'),
    url(r'^write/$',  views.ArticleCreate.as_view(), name='write'),
    url(r'^edit/(?P<pk>[\d]+)/$', views.ArticleUpdate.as_view(), name='edit'),
]