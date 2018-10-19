from django.conf.urls import url

from .views import (add_category, delete_category, edit_category,
                    get_all_articles_by_category, get_all_category,
                    manage_category)

app_name = 'category'

urlpatterns = [
    url(r'dashboard/$', manage_category, name='manage'),
    url(r'add/$', add_category, name='add'),
    url(r'edit/(?P<name>[-_\w\s]+)/$', edit_category, name='edit'),
    url(r'delete/(?P<name>[-_\w\s]+)/$', delete_category, name='delete'),
]

# urlpatterns used by backend
urlpatterns += [
    url(r'^all/$', get_all_category, name='all_category'),
    url(
        r'^(?P<name>[-_\w\s]+)/$',
        get_all_articles_by_category,
        name='all_article'
        ),
]
