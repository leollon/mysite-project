import debug_toolbar

from django.conf.urls import url, include
from .base import sitemaps, urlpatterns

urlpatterns = [url(r"^debug/", include(debug_toolbar.urls))] + urlpatterns
