import os
import socket
from getpass import getuser
from pathlib import Path

from celery.schedules import crontab

from .common import (ALLOWED_CONTENT, AUTH_PASSWORD_VALIDATORS,
                     AUTH_USER_MODEL, AUTHENTICATION_BACKENDS, BASE_DIR,
                     DATETIME_FORMAT_STRING, INSTALLED_APPS, LANGUAGE_CODE,
                     MIDDLEWARE, NAME_PATTERN, PASSWORD_HASHERS, PER_PAGE,
                     SESSION_CACHE_ALIAS, SESSION_ENGINE, SITE_ID,
                     TAGS_ARRAY_PATTERN, TAGS_FILTER_PATTERN,
                     TAGS_WHITESPACE_PATTERN, TEMPLATES, TIME_ZONE,
                     TITLE_PATTERN, USE_I18N, USE_L10N, USE_TZ,
                     WSGI_APPLICATION)

# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "p5cuwb&=cb^_jq3=s8lu8b4v*+_zfs7dh$%ij#_5@ca3jijw2i"
SERIAL_SECRET_KEY = "3NGKnEpCAauyEFZjbFQTTjrSAuQPVUqE89N5WJBawQMGJUjAhF"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DOMAIN_NAME = "http://127.0.0.1:8000"

ROOT_URLCONF = "mysite.config.urls.develop"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "blog",
        "HOST": "mysql",
        "port": 3306,
        "USER": "blog",
        "PASSWORD": "123456",
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
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# tied to app's static, like my_app/static/
STATIC_URL = "/static/"

# Directory containing all collected static files
STATIC_ROOT = (Path("/home/") / getuser() / "static").as_posix()

# Captcha's directory
CAPTCHA_DIR = Path(Path(BASE_DIR).parent.parent) / "static/images" / "captcha"
CAPTCHA_CACHED_TIME = 60  # in second


STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "static/")
]

# EMAIL HOST
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_ACCOUNT = {
    "EMAIL_HOST_USER": os.environ.get("EMAIL_USER"),
    "EMAIL_HOST_PASSWORD": os.environ.get("EMAIL_PWD"),
}

EMAIL_RELATED = {
    "REG_NOTIFICATION_FILE": "notification",
    "PWD_CHANGE_NOTIFICATION_FILE": "pwd_change",
    "COMMENT_NOTIFICATION": "comment_notification_template",
}

CSRF_USE_SESSIONS = False  # store csrftoke in the session
CSRF_COOKIE_SECURE = False  # only sent with an HTTPS connection
CSRF_COOKIE_HTTPONLY = True  # csrftoken disallow to be read by JS in console.
CSRF_COOKIE_AGE = (
    7 * 24 * 60
)  # in seconds, it's valid for seven days when under development
CSRF_USE_SESSIONS = True
SESSION_COOKIE_AGE = 604800  # in seconds
SECURE_CONTENT_TYPE_NOSNIFF = True  # 'x-content-type-options: nosniff' header
SECURE_BROWSER_XSS_FILTER = True  # 'x-xss-protection: 1; mode=block' header
SESSION_COOKIE_SECURE = False  # Using a secure-only session cookie
X_FRAME_OPTIONS = (
    "DENY"
)  # unless there is a good reason for your site to serve other parts of itself in a frame, you should change it to 'DENY'

ADMINS = [("root", "email@gmail.com")]
IMPORT_ARTICLE_USER = {
    "username": "root",
    "email": "email@gmail.com",
    "password": "admin1234",
}

# related to django-rest-framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
}

# celery-relate configuration
CELERY_BROKER_URL = "redis://redis:6379/1"

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
timezone = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    "debug-periodic-task": {
        "task": "apps.captcha.tasks.debug_periodic_task",
        "schedule": crontab(minute="*/1"),
        "args": ("[Periodic task]",),
    },
    "remove-outdated-captcha-image": {
        "task": "apps.captcha.tasks.remove_outdated_captcha_image",
        "schedule": crontab(minute="*/1"),
    },
}

# Logger: show more details
LOG_LEVEL = "DEBUG"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "[%(levelname)s] [%(asctime)s] [%(module)s] pid:%(process)d [%(message)s]"
        },
        "simple": {"format": "[%(levelname)s pid:%(process)d [%(message)s]"},
    },
    "loggers": {
        "": {
            "level": "WARNING",
            "handlers": ["console", "file", "mail_admins"],
            "propagate": True,
        },
        "django": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file", "mail_admins"],
            "propagate": True,
        },
        "django.server": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file", "mail_admins"],
            "propagate": True,
        },
        "django.template": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file", "mail_admins"],
            "propagate": True,
        },
        "django.request": {
            "level": "ERROR",
            "handlers": ["file", "mail_admins"],
            "propagate": False,
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["file", "mail_admins"],
            "propagate": False,
        },
    },
    # Control over which log records are passed from logger to handler.
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": str(
                Path(BASE_DIR).parent.parent / "log" / "mysite.log"
            ),
            "filters": ["require_debug_true"],
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_true"],
            "include_html": True,
        },
    },
}

INTERNAL_IPS = [
    "127.0.0.1",
    socket.gethostbyname(socket.gethostname())[:-1] + "1",
]
