from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-h!e@s1#z0(9+axm5xv0&8+i@e^crl+2@(s@h^53zgpg9^p^8mw"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "django_select2",
    "dashboard",
    "accounts",
    "school",
    "officers",
    "reportlab",
    "core",
    "xhtml2pdf",
    "teams",
    "easy_thumbnails",
    "image_cropping",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "accounts.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "primary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "primary.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "primary",
        "USER": "root",
        "PASSWORD": "Remmystar@48.com",
        "HOST": "localhost",  # or the hostname where your MySQL server is running
        "PORT": "3306",  # or the port on which your MySQL server is listening
    }
}

# Custom 404 page
# handler404 = "account.views.custom_404"
# settings.py

AIRTEL_MONEY_CLIENT_ID = "33c1cff0-45c8-4919-9aea-7e872eb2306f"
AIRTEL_MONEY_CLIENT_SECRET = "6c52463f-8235-45ba-89c6-6dcd6f1da33e"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Kampala"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin"


# settings.py

STATIC_URL = "/static/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
USE_DJANGO_JQUERY = True


# settings.py==========smtp
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "ssekittoshafiq@gmail.com"  # Your Gmail address
EMAIL_HOST_PASSWORD = "gyow rrgb nxvu mktx"  # Use the generated app password

# maintenance mode
MAINTENANCE_MODE = False
# from easy_thumbnails.conf import Settings as thumbnail_settings
from easy_thumbnails.conf import Settings as thumbnail_settings

THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + thumbnail_settings.THUMBNAIL_PROCESSORS

IMAGE_CROPPING_BACKEND = "image_cropping.backends.easy_thumbs.EasyThumbnailsBackend"
IMAGE_CROPPING_BACKEND_PARAMS = {}