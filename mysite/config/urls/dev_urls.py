from mysite.config.urls.base import *
import debug_toolbar

urlpatterns += [
    url('^__debug__/', include(debug_toolbar.urls)),
]