# -*- encoding: utf-8 -*-

import os, sys

sys.path.insert(0, '..')

PROJECT_ROOT = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test'
    }
}

MIDDLEWARE_CLASSES = ()

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = ()

SECRET_KEY = 'di!n($kqa3)nd%ikad#kcjpkd^uw*h%*kj=*pm7$vbo6ir7h=l'
INSTALLED_APPS = (
    'djmail',
    'djcelery',
    'testing',
)

import djcelery
djcelery.setup_loader()

CELERY_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'
