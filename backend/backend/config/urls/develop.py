import debug_toolbar
from django.conf.urls import include, url

from .base import urlpatterns

urlpatterns = [url(r"^debug/", include(debug_toolbar.urls))] + urlpatterns
