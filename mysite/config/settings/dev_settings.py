import os
from getpass import getuser
from pathlib import Path

from mysite.config.settings.common import (
    BASE_DIR, INSTALLED_APPS, TEMPLATES, MIDDLEWARE, WSGI_APPLICATION,
    AUTH_PASSWORD_VALIDATORS, PASSWORD_HASHERS, LANGUAGE_CODE, TIME_ZONE,
    USE_I18N, USE_L10N, USE_TZ, PER_PAGE, ALLOWED_CONTENT, AUTH_USER_MODEL,
    AUTHENTICATION_BACKENDS, SITE_ID)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

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

ROOT_URLCONF = 'mysite.config.urls.dev_urls'

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# tied to app's static, like my_app/static/
STATIC_URL = '/static/'

# Directory containing all static files
STATIC_ROOT = str(Path('/home/') / getuser() / 'static')

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static/')
]

# EMAIL HOST
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

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

INTERNAL_IPS = ('127.0.0.1', )
