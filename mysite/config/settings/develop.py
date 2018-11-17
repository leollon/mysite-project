import os

from getpass import getuser
from pathlib import Path

from mysite.config.settings.common import (
    BASE_DIR, INSTALLED_APPS, TEMPLATES, MIDDLEWARE, WSGI_APPLICATION,
    AUTH_PASSWORD_VALIDATORS, PASSWORD_HASHERS, LANGUAGE_CODE, TIME_ZONE,
    USE_I18N, USE_L10N, USE_TZ, PER_PAGE, ALLOWED_CONTENT, AUTH_USER_MODEL,
    AUTHENTICATION_BACKENDS, SITE_ID, ADMINS)

# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p5cuwb&=cb^_jq3=s8lu8b4v*+_zfs7dh$%ij#_5@ca3jijw2i'
SERIAL_SECRET_KEY = '3NGKnEpCAauyEFZjbFQTTjrSAuQPVUqE89N5WJBawQMGJUjAhF'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DOMAIN_NAME = "http://127.0.0.1:8000"

ROOT_URLCONF = 'mysite.config.urls.develop'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'blog',
        "PASSWORD": '123456'
    }
}

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# tied to app's static, like my_app/static/
STATIC_URL = '/static/'

# Directory containing all static files
STATIC_ROOT = str(Path('/home/') / getuser() / 'static')

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static/')
]

# Cache-related
SESSION_CACHE_ALIAS = "redis"
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# EMAIL HOST
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_ACCOUNT = {
    'EMAIL_HOST_USER': os.environ.get("EMAIL_USER"),
    'EMAIL_HOST_PASSWORD': os.environ.get('EMAIL_PWD')
}

EMAIL_RELATED = {
    'REG_NOTIFICATION_FILE': 'notification',
    'PWD_CHANGE_NOTIFICATION_FILE': 'pwd_change',
    'COMMENT_NOTIFICATION': 'comment_notification_template',
}

CSRF_USE_SESSIONS = True  # store csrftoke in the session
CSRF_COOKIE_SECURE = False  # only sent with an HTTPS connection
CSRF_COOKIE_HTTPONLY = True  # csrftoken disallow to be read by JS in console.
CSRF_COOKIE_AGE = 604800  # in seconds
CSRF_USE_SESSIONS = True
SESSION_COOKIE_AGE = 604800  # in seconds
SECURE_CONTENT_TYPE_NOSNIFF = True # 'x-content-type-options: nosniff' header
SECURE_BROWSER_XSS_FILTER = True # 'x-xss-protection: 1; mode=block' header
SESSION_COOKIE_SECURE = True # Using a secure-only session cookie
X_FRAME_OPTIONS = 'DENY' # unless there is a good reason for your site to serve other parts of itself in a frame, you should change it to 'DENY'

# Logger: show more details
LOG_LEVEL = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s] pid:%(process)d [%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s pid:%(process)d [%(message)s]'
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': True,
        },
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': True,
        },
        'django.request': {
            'level': "ERROR",
            'handlers': ['file', 'mail_admins'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': "ERROR",
            'handlers': ['file', 'mail_admins'],
            'propagate': False,
        },
    },
    # Control over which log records are passed from logger to handler.
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': "ERROR",
            'class': 'logging.FileHandler',
            'filename': str(Path(BASE_DIR).parent / 'log' / 'develop.log'),
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': "ERROR",
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true'],
            'include_html': True,
        }
    },
}

INTERNAL_IPS = ('127.0.0.1', )
