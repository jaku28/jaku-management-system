"""Local settings for development."""

from .base import *  # noqa

ALLOWED_HOSTS = ['*',]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'tmp', 'email')


# Application definition

INSTALLED_APPS += [
    'debug_toolbar',
]

# flake8: noqa F405
