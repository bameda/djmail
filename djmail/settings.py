import os
import dj_database_url

SECRET_KEY = 'p23jof024jf5-94j3f023jf230=fj234fp34fijo'

DEBUG = True

# docker run -d -p 5432:5432 -v /var/lib/postgresql postgres
DATABASES = {}
DATABASES['default'] = dj_database_url.config(default='postgres://postgres@localhost:5432/postgres')

INSTALLED_APPS = [
    'djmail',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_SERIALIZER = 'json'
