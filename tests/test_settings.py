# -*- encoding: utf-8 -*-

SECRET_KEY = 'p23jof024jf5-94j3f023jf230=fj234fp34fijo'

# docker run -d -p 5432:5432 postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

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
