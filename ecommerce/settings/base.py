"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.2.1 and python 3.10.9

"""

from pathlib import Path
from decouple import config
import dj_database_url







# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY ="django-insecure-fz(terk0ud&3tuf=a^=-h3yl+3)8&3c(-$4_--h&93vcgva2^0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default="True")

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    
    
    
    "ecommerce.apps.account",
    "ecommerce.apps.products",
    "ecommerce.apps.contact",
    "ecommerce.apps.search",
    "ecommerce.apps.cart",
    "ecommerce.apps.social",
    "ecommerce.apps.shop",
    "ecommerce.apps.instagram",
    "ecommerce.apps.about",
    "ecommerce.apps.blog",
    "ecommerce.apps.marketing",
    "ecommerce.apps.order",
    "ecommerce.apps.billing",
    "ecommerce.apps.addresses",
    "ecommerce.apps.analytics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "ecommerce.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': dj_database_url.parse(config("DATABASE_URL"))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Africa/Casablanca"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR.parent.parent / "static"

STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)




MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR.parent.parent / "media"






# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "fr_FR",  # To force a specific language instead of the Django current language.
}





USE_THOUSAND_SEPARATOR = True 

# AUTH_USER_MODEL = 'accounts.User'

LOGOUT_REDIRECT_URL = "/login/"
LOGOUT_REDIRECT_URL = "/"  # new

SIMPLE_ENVIRONMENT = config("SIMPLE_ENVIRONMENT", default="local")


# MAILCHIMP CREDENTIALS
MAILCHIMP_API_KEY = "e3a7bc63e4b0cfda697e18ec938a44be-us20"
MAILCHIMP_DATA_CENTER = "us20"
MAILCHIMP_EMAIL_LIST_ID = "a9e03c576c"



# AUTH_USER_MODEL = 'account.User'
# LOGIN_URL = 'accounts:login'
# LOGIN_URL_REDIRECT = '/'
# LOGOUT = 'accounts:logout'

# AUTH_USER_MODEL = "accounts.CustomUser"  # ne


FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_END_SESSION = False




MANAGERS = (
    ('abdul', 'abdul@gmail.com')
)






EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='localhost')
EMAIL_USER_TLS = config("EMAIL_USER_TLS", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default='')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default='')





ADMINS = MANAGERS
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
