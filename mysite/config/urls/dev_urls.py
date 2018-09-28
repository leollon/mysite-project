import debug_toolbar

from mysite.config.urls.base import *

urlpatterns += [
    url('^__debug__/', include(debug_toolbar.urls)),
]
