import getpass
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from mysite.config.settings.common import *

environ = {
    'SECRET_KEY': "this_key_is_needed_by_django.",
    'SERIAL_SECRET_KEY': "this_key_is_for_itsdangerous",
    'DB_USER': "your_DB_user",
    'DB_PWD': "your_DB_password",
    'EMAIL_USER': "your_email_account",
    'EMAIL_PWD': "your_email_authentication_password",
    'EMAIL_HOST': "your_email_host",
}


SECRET_KEY = environ.get('SECRET_KEY')
SERIAL_SECRET_KEY = environ.get('SERIAL_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['your_test_domain_name']

DOMAIN_NAME = ALLOWED_HOSTS[0]

ROOT_URLCONF = 'mysite.config.urls.production'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PWD'),
    }
}


# Directory containing all static files
# when running `python manage.py collectstatic`, collect all static file in a
# same directory.
# for production deployed, use nginx to response static file requested
STATIC_ROOT = os.path.join(os.path.join('/home/', getpass.getuser()), 'assets')


# Here stores all static files
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'assets')
]

# Show the articles' number in each page
PER_PAGE = 6

# In order to preventing XSS, it needs to set `ALLOWED_CONTENT`
ALLOWED_CONTENT = {
    'ALLOWED_TAGS': ['blockquote', 'ul', 'li', 'ol', 'pre', 'code',
                     'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a',
                     'q', 'section', 'img', 'table', 'thead', 'tbody',
                     'tr', 'th', 'td'],
    'ALLOWED_ATTRIBUTES': {'*': ['class', 'style'],
                           'a': ['href'],
                           'img': ['src', 'alt', 'width', 'height'], },
    'ALLOWED_STYLES': ['color', 'background-image', 'background',
                       'font', 'text-align', ]
}

# Customize user model
AUTH_USER_MODEL = 'users.User'

# Customize backend authentication
AUTHENTICATION_BACKENDS = [
    'apps.users.backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Email account
EMAIL_ACCOUNT = {
    'EMAIL_HOST_USER': environ.get("EMAIL_USER"),
    'EMAIL_HOST_PASSWORD': environ.get('EMAIL_PWD')
}


# Email server related
EMAIL_HOST = environ.get('EMAIL_HOST')
EMAIL_PORT = environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True

# Email message content template related
EMAIL_RELATED = {
    'REG_NOTIFICATION_FILE': 'notification',
    'PWD_CHANGE_NOTIFICATION_FILE': 'pwd_change',
    'COMMENT_NOTIFICATION': 'comment_notification_template',
}


CSRF_USE_SESSIONS = True  # store csrftoke in the session
CSRF_COOKIE_SECURE = True  # only sent with an HTTPS connection
CSRF_COOKIE_HTTPONLY = True  # csrftoken disallow to be read by JS in console
CSRF_COOKIE_AGE = 604800  # in seconds
SESSION_COOKIE_AGE = 604800  # in seconds

sentry_sdk.init(
    dsn="",
    integrations=[DjangoIntegration()]
)