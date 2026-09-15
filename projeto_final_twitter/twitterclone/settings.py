import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = any(
    os.getenv(name)
    for name in ("VERCEL", "VERCEL_ENV", "VERCEL_URL", "NOW_REGION")
)
PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME", "").strip()
IS_PYTHONANYWHERE = bool(PYTHONANYWHERE_USERNAME)
IS_PRODUCTION = IS_VERCEL or IS_PYTHONANYWHERE

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "twitter-clone-ebac-dev-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False" if IS_PRODUCTION else "True").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]
if IS_VERCEL and ".vercel.app" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".vercel.app")
if IS_PYTHONANYWHERE:
    pythonanywhere_host = f"{PYTHONANYWHERE_USERNAME}.pythonanywhere.com"
    if pythonanywhere_host not in ALLOWED_HOSTS:
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
    "social",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "twitterclone.urls"

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

WSGI_APPLICATION = "twitterclone.wsgi.application"
ASGI_APPLICATION = "twitterclone.asgi.application"

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
if POSTGRES_HOST:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "twitterclone"),
            "USER": os.getenv("POSTGRES_USER", "twitterclone"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "twitterclone"),
            "HOST": POSTGRES_HOST,
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": 60,
        }
    }
elif IS_VERCEL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/twitterclone.sqlite3",
            "OPTIONS": {"timeout": 20},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = Path("/tmp/twitterclone-media") if IS_VERCEL else BASE_DIR / "media"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "feed"
LOGOUT_REDIRECT_URL = "login"

# Na Vercel evitamos depender da tabela django_session para páginas públicas.
# No PythonAnywhere o SQLite/PostgreSQL é persistente e usa as sessões normais do Django.
if IS_VERCEL:
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
elif IS_PYTHONANYWHERE:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if IS_VERCEL and "https://*.vercel.app" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("https://*.vercel.app")
if IS_PYTHONANYWHERE:
    pythonanywhere_origin = f"https://{PYTHONANYWHERE_USERNAME}.pythonanywhere.com"
    if pythonanywhere_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(pythonanywhere_origin)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
