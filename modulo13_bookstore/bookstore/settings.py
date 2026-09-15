import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

IS_VERCEL = os.getenv("VERCEL") == "1"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "ebac-modulo13-bookstore-dev")
DEBUG = os.getenv("DJANGO_DEBUG", "0" if IS_VERCEL else "1").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1,web,.vercel.app",
    ).split(",")
    if host.strip()
]

pythonanywhere_host = os.getenv("PYTHONANYWHERE_HOST", "").strip()
if pythonanywhere_host and pythonanywhere_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(pythonanywhere_host)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "store",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "bookstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "bookstore" / "templates"],
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

WSGI_APPLICATION = "bookstore.wsgi.application"

POSTGRES_HOST = os.getenv("POSTGRES_HOST")

if POSTGRES_HOST:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "bookstore"),
            "USER": os.getenv("POSTGRES_USER", "bookstore"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "bookstore"),
            "HOST": POSTGRES_HOST,
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
elif IS_VERCEL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/bookstore.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = ["127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "store.pagination.BookstorePagination",
    "PAGE_SIZE": 5,
}
