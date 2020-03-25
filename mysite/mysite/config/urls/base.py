"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.contrib.flatpages import views as flatpage_views
from django.contrib.sitemaps import views as sitemap_views
from django.urls import re_path
from django.views.decorators.cache import cache_page

from ..sitemaps import ArticleSiteMap

sitemaps = {"Article": ArticleSiteMap}

urlpatterns = [
    re_path(r"^accounts/backstage/", admin.site.urls),
    re_path(r"^api/v1/", include("apps.urls")),
    re_path(
        r"^sitemap\.xml$",
        cache_page(60 * 60 * 24 * 7, cache="redis")(sitemap_views.sitemap),
        {"sitemaps": sitemaps},
    ),
    re_path(
        r"^(?P<url>.*/)$",
        cache_page(60 * 60 * 24 * 7, cache="redis")(flatpage_views.flatpage),
        name="django.contrib.flatpages.views.flatpage",
    ),
]
