"""Stage settings."""

import os
from urllib.parse import urlparse

import dj_database_url

import raven

from .base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

ALLOWED_HOSTS = ['.herokuapp.com', '.appweb.net']

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware'
]


# Application definition

INSTALLED_APPS += [
    'storages',
	'django.contrib.postgres',
    'raven.contrib.django.raven_compat',
]

# SSL/HTTPS
# https://docs.djangoproject.com/en/1.11/topics/security/#ssl-https

SECURE_SSL_REDIRECT = True


# Sentry

SENTRY_DSN = os.environ.get('SENTRY_DSN')

RAVEN_CONFIG = {
    'site': os.environ.get('HEROKU_APP_NAME')
}


# Database

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


# Static files (Whitenoise)

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

WHITENOISE_STATIC_PREFIX = STATIC_URL

STATIC_URL = os.environ.get('DJANGO_STATIC_HOST', STATIC_URL)


# Media files (AWS Settings)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Email settings
 
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# flake8: noqa F405
