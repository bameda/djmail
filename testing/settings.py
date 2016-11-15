# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

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
    'testing',
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


CELERY_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'


# docker run -d --hostname my-rabbit -p 5672:5672 --name my-rabbit rabbitmq:3
#CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# docker run --name my-redis -p 6379:6379 -d redis
CELERY_RESULT_BACKEND = 'redis://'

EMAIL_BACKEND = 'djmail.backends.celery.EmailBackend'

# run celery worker (run in the parent djmail directory, not in the testing subdir):
# celery -A djmail worker -l info