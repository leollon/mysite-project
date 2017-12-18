from django.conf.urls import url
from article_category.views import get_all_articles_by_category
from article_category.views import get_all_category

app_name = 'category'

urlpatterns = [
    url(r'^all/$', get_all_category, name='all_category'),
    url(r'^(?P<category_id>[\d]+)/$',
        get_all_articles_by_category,
        name='all_article'),
]

