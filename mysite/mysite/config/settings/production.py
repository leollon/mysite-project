import os
from getpass import getuser
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import (
    ALLOWED_CONTENT,
    AUTH_PASSWORD_VALIDATORS,
    AUTH_USER_MODEL,
    AUTHENTICATION_BACKENDS,
    BASE_DIR,
    DATETIME_FORMAT_STRING,
    INSTALLED_APPS,
    LANGUAGE_CODE,
    MIDDLEWARE,
    NAME_PATTERN,
    PASSWORD_HASHERS,
    PER_PAGE,
    SESSION_CACHE_ALIAS,
    SESSION_ENGINE,
    SITE_ID,
    TAGS_ARRAY_PATTERN,
    TAGS_FILTER_PATTERN,
    TAGS_WHITESPACE_PATTERN,
    TEMPLATES,
    TIME_ZONE,
    TITLE_PATTERN,
    USE_I18N,
    USE_L10N,
    USE_TZ,
    WSGI_APPLICATION,
)

environ = {
    "SECRET_KEY": "ao$DZM2C9KlGksl&Lzl$7Tx0TOlEXoCyZxg7i&6b3LliqRFXHk1YinXBID@B#Ncm",
    "SERIAL_SECRET_KEY": "e885Lufnp24ux@iIMJ2HSC^Og2CTO^fU8y93gd6Y4IRbPlJFV^BL$e9MWTpGMnw&",
    "DB_USER": "blog",
    "DB_PWD": "123456",
    "EMAIL_USER": "your_email_account",
    "EMAIL_PWD": "your_email_authentication_password",
    "EMAIL_HOST": "your_email_host",
    "EMAIL_PORT": 587,
}

SECRET_KEY = environ.get("SECRET_KEY")
SERIAL_SECRET_KEY = environ.get("SERIAL_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["dp.demo.com", "127.0.0.1"]

DOMAIN_NAME = ALLOWED_HOSTS[0]

ROOT_URLCONF = "mysite.config.urls.production"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "blog",
        "HOST": "mysql",
        "PORT": "3306",
        "USER": environ.get("DB_USER"),
        "PASSWORD": environ.get("DB_PWD"),
        "CHARSET": "utf8mb4",
        "COLLATION": "utf8mb4_unicode_ci",
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

# Directory containing all static files
# when running `python manage.py collectstatic`, collect all static file in a
# same directory.
# for production deployed, use nginx to response static file requested
STATIC_ROOT = (Path("/home/") / getuser() / "assets").as_posix()

# Captcha's directory
CAPTCHA_DIR = Path(Path(BASE_DIR).parent.parent) / "assets/images" / "captcha"
CAPTCHA_CACHED_TIME = 30 * 60  # in second

# Here stores all static files
STATICFILES_DIRS = [os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "assets")]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Email account
EMAIL_ACCOUNT = {"EMAIL_HOST_USER": environ.get("EMAIL_USER"), "EMAIL_HOST_PASSWORD": environ.get("EMAIL_PWD")}

# Email server related
EMAIL_HOST = environ.get("EMAIL_HOST")
EMAIL_PORT = environ.get("EMAIL_PORT")
EMAIL_USE_TLS = True

# Email message content template related
EMAIL_RELATED = {
    "REG_NOTIFICATION_FILE": "notification",
    "PWD_CHANGE_NOTIFICATION_FILE": "pwd_change",
    "COMMENT_NOTIFICATION": "comment_notification_template",
}

CSRF_USE_SESSIONS = False  # store csrftoke in the session
CSRF_COOKIE_SECURE = False  # only sent with an HTTPS connection
CSRF_COOKIE_HTTPONLY = True  # csrftoken disallow to be read by JS in console
CSRF_COOKIE_AGE = 15 * 60  # in seconds
SESSION_COOKIE_AGE = 7 * 24 * 60  # in seconds
SECURE_CONTENT_TYPE_NOSNIFF = True  # x-content-type-options: nosniff header
SECURE_BROWSER_XSS_FILTER = True  # x-xss-protection: 1; mode=block header
SESSION_COOKIE_SECURE = False  # Using a secure-only session cookie
X_FRAME_OPTIONS = (
    "DENY"
)  # unless there is a good reason for your site to serve other parts of itself in a frame, you should change it to 'DENY'

# related to django-rest-framework
REST_FRAMEWORK = {"DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)}
ADMINS = [("root", "email@gmail.com")]
IMPORT_ARTICLE_USER = {"username": "root", "email": "email@gmail.com", "password": "admin1234"}


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
            "filename": (Path(BASE_DIR).parent.parent / "var/log" / "mysite.log").as_posix(),
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


sentry_sdk.init(dsn="", integrations=[DjangoIntegration()], server_name="mysite")
