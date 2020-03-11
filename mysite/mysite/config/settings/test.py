from .develop import *  # noqa

DEBUG = False

PASSWORD_HASHERS = [  # noqa
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'  # noqa
