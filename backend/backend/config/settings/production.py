from os import environ
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import (  # noqa: F401
    AUTH_PASSWORD_VALIDATORS, AUTH_USER_MODEL, AUTHENTICATION_BACKENDS,
    BASE_DIR, CATEGORY_FILTER_PATTERN, CATEGORY_PATTERN,
    DATETIME_FORMAT_STRING, DATETIME_PATTERN, INSTALLED_APPS, LANGUAGE_CODE,
    MIDDLEWARE, PASSWORD_HASHERS, SESSION_CACHE_ALIAS, SESSION_ENGINE, SITE_ID,
    TAGS_ARRAY_PATTERN, TAGS_FILTER_PATTERN, TAGS_WHITESPACE_PATTERN,
    TEMPLATES, TIME_ZONE, TITLE_PATTERN, USE_I18N, USE_L10N, USE_TZ,
    WSGI_APPLICATION,
)

SECRET_KEY = environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['*']

HOST = ALLOWED_HOSTS[0]

ROOT_URLCONF = "backend.config.urls.production"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ.get("PG_USER_DB"),
        "HOST": environ.get("POSTGRES_HOST"),
        "port": environ.get("POSTGRES_PORT"),
        "USER": environ.get("PG_USER"),
        "PASSWORD": environ.get("PG_USER_PASSWORD"),
        "CHARSET": "utf8",
        "ATOMIC_REQUESTS": True,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "options": {"MAX_ENTRIES": 1024},
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# tied to app's static, like my_app/static/
STATIC_URL = "/assets/"

# Here stores all static files
STATICFILES_DIRS = [(Path(BASE_DIR).parent.parent / "assets/").as_posix(), ]

# Directory containing all static files
# when running `python manage.py collectstatic`, collect all static file into
# a same directory. For production, use nginx to response static file requested
STATIC_ROOT = (Path(BASE_DIR).parent.parent / "dj_assets").as_posix()

# Captcha's directory# Captcha's directory
CAPTCHA_BASE_DIR = (Path(BASE_DIR).parent.parent / "assets/images/captcha").as_posix()
CAPTCHA_CACHED_TIME = 30 * 60  # in second

TOKEN_EXPIRES_IN = 30 * 60  # thirty minutes in total


# EMAIL
EMAIL_HOST_USER = environ.get("EMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = environ.get("EMAIL_PASSWORD")
EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_PORT = environ.get("EMAIL_PORT")
EMAIL_USE_TLS = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# store csrftoke in the session
CSRF_USE_SESSIONS = False
# only sent with an HTTPS connection
CSRF_COOKIE_SECURE = False
# csrftoken disallow to be read by JS in console
CSRF_COOKIE_HTTPONLY = True
# in seconds
CSRF_COOKIE_AGE = 15 * 60
# in seconds
SESSION_COOKIE_AGE = 7 * 24 * 60
# x-content-type-options: nosniff header
SECURE_CONTENT_TYPE_NOSNIFF = True
# x-xss-protection: 1; mode=block header
SECURE_BROWSER_XSS_FILTER = True
# Using a secure-only session cookie
SESSION_COOKIE_SECURE = False
# unless there is a good reason for your site to serve other parts of itself in
# a frame, you should change it to 'DENY'
X_FRAME_OPTIONS = "DENY"

ADMINS = [("root", "email@gmail.com")]
IMPORT_ARTICLE_USER = {"username": "root", "email": "email@gmail.com", "password": "admin1234"}

# related to django-rest-framework
REST_FRAMEWORK = {"DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)}

# celery-relate configuration
CELERY_BROKER_URL = "redis://redis:6379/0"

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
timezone = TIME_ZONE

# Logger: error loglevel
LOG_LEVEL = "ERROR"


def create_log_file():
    (Path(BASE_DIR).parent.parent / "var/log").mkdir(parents=True, exist_ok=True)
    (Path(BASE_DIR).parent.parent / "var/log" / "backend.log").touch()
    return (Path(BASE_DIR).parent.parent / "var/log" / "backend.log").as_posix()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {"format": "[%(levelname)s] [%(asctime)s] [%(module)s] pid:%(process)d [%(message)s]"},
        "simple": {"format": "[%(levelname)s pid:%(process)d [%(message)s]"},
    },
    "loggers": {
        "": {"level": "WARNING", "handlers": ["file"], "propagate": True},
        "django": {"level": LOG_LEVEL, "handlers": ["file"], "propagate": True},
        "django.template": {"level": LOG_LEVEL, "handlers": ["file"], "propagate": True},
        "django.request": {"level": LOG_LEVEL, "handlers": ["file"], "propagate": False},
        "django.db.backends": {"level": LOG_LEVEL, "handlers": ["file"], "propagate": False},
    },
    # Control over which log records are passed from logger to handler.
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": create_log_file(),
            "filters": ["require_debug_false"],
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "include_html": True,
        },
    },
}


sentry_sdk.init(dsn="", integrations=[DjangoIntegration()], server_name="backend")
