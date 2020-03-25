import re
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent.as_posix()

# Application definition and Customized APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "rest_framework",
    "apps.article.apps.ArticleConfig",
    "apps.category.apps.ArticleCategoryConfig",
    "apps.user.apps.UserConfig",
    "apps.comment.apps.CommentConfig",
    "apps.captcha.apps.CaptchaConfig",
    "apps.mail.apps.MailConfig",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            Path(BASE_DIR).parent.parent.joinpath("mail_templates").as_posix(),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

MIDDLEWARE = [
    # native middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # customized middleware
    "apps.core.middleware.OnlineMiddleware",
]

WSGI_APPLICATION = "mysite.config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# Password Encrypt Hasher
PASSWORD_HASHERS = ["django.contrib.auth.hashers.BCryptSHA256PasswordHasher"]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Singapore"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Customize User model
AUTH_USER_MODEL = "user.User"

# Customize backend authentication
AUTHENTICATION_BACKENDS = [
    "apps.user.backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Cache-related
SESSION_CACHE_ALIAS = "redis"
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SITE_ID = 1

DATETIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"
# 获取文章标题
TITLE_PATTERN = re.compile(
    r"title:\ *([\w\d\-,.!?'\"&/<>:\ \u4e00-\u9fa5\u30a0-\u30ff\u3040-\u309f\u4e00-\u9fcf\(\)\[\]]*)\s*"
)
# 获取时间
DATETIME_PATTERN = re.compile(r"date:\ *(\d{4}\-\d{2}\-\d{2}\ *\d{2}:\d{2}:\d{2})\s*")
# 获取文章分类名字
CATEGORY_PATTERN = re.compile(
    r"categor(?:y|ies):\ *([\w\d\-'\ \[\]/.\u4e00-\u9fa5\u30a0-\u30ff\u3040-\u309f\u4e00–\u9fcf]*)\s*")
CATEGORY_FILTER_PATTERN = re.compile(r'[^\-\w\d]+')
# 获取文章的标签
TAGS_ARRAY_PATTERN = re.compile(
    r"tags:\ *\[([\w\d\ \-.\"',/\u4e00-\u9fa5\u30a0-\u30ff\u3040-\u309f\u4e00–\u9fcf]*)\]\s*")
# 文章标签过滤规则
TAGS_WHITESPACE_PATTERN = re.compile(r"(?:,+\s*)")  # 去除逗号后面多余的空格
TAGS_FILTER_PATTERN = re.compile(r"[^\w\d\ \-,]+")  # 去除无效字符
