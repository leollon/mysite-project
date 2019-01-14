import debug_toolbar

from django.conf.urls import url, include
from mysite.config.urls.base import sitemaps, urlpatterns

urlpatterns += [
    url('^__debug__/', include(debug_toolbar.urls)),
]