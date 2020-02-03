from django.conf.urls import url

from .views import CategorizeArticleListView, CategoryListView

app_name = 'category'

# urlpatterns for site visistor
urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='all_category'),
    url(r'^(?P<name>[\-\w\d\ ]+)/$',
        CategorizeArticleListView.as_view(),
        name='all_article'),
]
