from mysite.config.settings.common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p5cuwb&=cb^_jq3=s8lu8b4v*+_zfs7dh$%ij#_5@ca3jijw2i'
SERIAL_SECRET_KEY = '3NGKnEpCAauyEFZjbFQTTjrSAuQPVUqE89N5WJBawQMGJUjAhF'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

DOMAIN_NAME = "http://127.0.0.1:8000"

ROOT_URLCONF = 'mysite.config.urls.dev_urls'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

INTERNAL_IPS = ('127.0.0.1',)
