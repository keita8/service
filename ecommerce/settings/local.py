# flake8: noqa

from .base import *

# INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
import os

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_my_proj')
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")
PROTECTED_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "protected_media")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

CORS_REPLACE_HTTPS_REFERER = False
HOST_SCHEME = 'http://'
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False








# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"