from django.conf.urls import url

from .views import (CategorizeArticleListView, CategoryListView, add_category,
                    delete_category, edit_category, manage_category)

app_name = 'category'

# urlpatterns for backend management
urlpatterns = [
    url(r'dashboard/$', manage_category, name='manage'),
    url(r'add/$', add_category, name='add'),
    url(r'edit/(?P<name>[\-\w\s]+)/$', edit_category, name='edit'),
    url(r'delete/(?P<name>[\-\w\s]+)/$', delete_category, name='delete'),
]

# urlpatterns for site visistor
urlpatterns += [
    url(r'^$', CategoryListView.as_view(), name='all_category'),
    url(r'^(?P<name>[\-\w\s]+)/$',
        CategorizeArticleListView.as_view(),
        name='all_article'),
]
