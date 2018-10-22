import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition and Customized APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',
    'apps.article.apps.ArticleConfig',
    'apps.category.apps.ArticleCategoryConfig',
    'apps.users.apps.UsersConfig',
    'apps.comment.apps.CommentConfig',
]

TEMPLATES = [
    {
        'BACKEND':
        'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(
                os.path.dirname(os.path.dirname(BASE_DIR)), 'templates/')
        ],
        'APP_DIRS':
        True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

WSGI_APPLICATION = 'mysite.config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Password Encrypt Hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Hongkong'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# tied to app's static, like my_app/static/
STATIC_URL = '/static/'

# Show the articles' number in each page
PER_PAGE = 6

# In order to preventing XSS, it needs to set `ALLOWED_CONTENT`
ALLOWED_CONTENT = {
    'ALLOWED_TAGS': [
        'blockquote', 'ul', 'li', 'ol', 'pre', 'code', 'p', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'a', 'q', 'section', 'img', 'table', 'thead',
        'tbody', 'tr', 'th', 'td', 'br'
    ],
    'ALLOWED_ATTRIBUTES': {
        '*': ['class', 'style'],
        'a': ['href'],
        'img': ['src', 'alt', 'width', 'height'],
    },
    'ALLOWED_STYLES': [
        'color',
        'background-image',
        'background',
        'font',
        'text-align',
    ]
}

# Customize User model
AUTH_USER_MODEL = 'users.User'

# Customize backend authentication
AUTHENTICATION_BACKENDS = [
    'apps.users.backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
