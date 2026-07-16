"""
Django settings for Anomaly_Detection project.
"""

from datetime import timedelta
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config( "DEBUG", cast=bool, default=False, )

ALLOWED_HOSTS = config( "ALLOWED_HOSTS", cast=lambda v: [host.strip() for host in v.split(",")], default="localhost", )

LANGUAGE_CODE = config( "LANGUAGE_CODE", default="en-us", )

TIME_ZONE = config( "TIME_ZONE", default="UTC", )

USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",

    "rest_framework",
    "drf_spectacular",

    "anomaly",
    "classification",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Anomaly_Detection.urls"

WSGI_APPLICATION = "Anomaly_Detection.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": config( "DB_ENGINE", default="django.db.backends.sqlite3", ),
        "NAME": config( "DB_NAME", default=str(BASE_DIR / "db.sqlite3"), ),
        "USER": config( "DB_USER", default="", ),
        "PASSWORD": config( "DB_PASSWORD", default="", ),
        "HOST": config( "DB_HOST", default="", ),
        "PORT": config( "DB_PORT", default="", ),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

STATIC_URL = config( "STATIC_URL", default="/static/", )

STATICFILES_DIRS = [ BASE_DIR / "static", ]

STATIC_ROOT = BASE_DIR / config( "STATIC_ROOT", default="staticfiles", )

MEDIA_URL = config( "MEDIA_URL", default="/media/", )

MEDIA_ROOT = BASE_DIR / config( "MEDIA_ROOT", default="media", )

LOG_LEVEL = config( "LOG_LEVEL", default="INFO", )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[{asctime}] {levelname} {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "errors.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "anomaly": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS":"rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
}

SPECTACULAR_SETTINGS = {
    "TITLE": config( "API_TITLE", default="Anomaly Detection API", ),
    "DESCRIPTION": config( "API_DESCRIPTION", default="API Documentation", ),
    "VERSION": config( "API_VERSION", default="1.0.0", ),
    "COMPONENT_SPLIT_REQUEST": True,
}

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=lambda v: [origin.strip() for origin in v.split(",")],
    default="http://localhost:5173,http://127.0.0.1:5173",
)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=lambda v: [origin.strip() for origin in v.split(",")],
    default="http://localhost:5173,http://127.0.0.1:5173",
)

SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_NAME = config( "SESSION_COOKIE_NAME", default="sessionid", )

SESSION_COOKIE_HTTPONLY = config( "SESSION_COOKIE_HTTPONLY", cast=bool, default=True, )

SESSION_COOKIE_SAMESITE = config( "SESSION_COOKIE_SAMESITE", default="Lax", )

SESSION_COOKIE_SECURE = config( "SESSION_COOKIE_SECURE", cast=bool, default=False, )

SESSION_SAVE_EVERY_REQUEST = config( "SESSION_SAVE_EVERY_REQUEST", cast=bool, default=True, )

SESSION_EXPIRE_AT_BROWSER_CLOSE = config( "SESSION_EXPIRE_AT_BROWSER_CLOSE", cast=bool, default=False, )

SECURE_BROWSER_XSS_FILTER = not DEBUG

SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG

X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = config( "SECURE_SSL_REDIRECT", cast=bool, default=False, )

SECURE_HSTS_SECONDS = config( "SECURE_HSTS_SECONDS", cast=int, default=0, )

SECURE_HSTS_INCLUDE_SUBDOMAINS = config( "SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool, default=False, )

SECURE_HSTS_PRELOAD = config( "SECURE_HSTS_PRELOAD", cast=bool, default=False, )

SIMPLE_JWT = {

    # Token lifetimes
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config( "JWT_ACCESS_TOKEN_MINUTES", cast=int, default=30, )
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config( "JWT_REFRESH_TOKEN_DAYS", cast=int, default=7, )
    ),

    # Refresh behavior
    "ROTATE_REFRESH_TOKENS": config( "JWT_ROTATE_REFRESH_TOKENS", cast=bool, default=True, ),

    "UPDATE_LAST_LOGIN": config( "JWT_UPDATE_LAST_LOGIN", cast=bool, default=False, ),

    # Authentication header
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

}