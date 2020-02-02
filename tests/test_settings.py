# -*- encoding: utf-8 -*-

SECRET_KEY = 'p23jof024jf5-94j3f023jf230=fj234fp34fijo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
    }
}

INSTALLED_APPS = [
    'djmail',
    'tests'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

CELERY_TASK_ALWAYS_EAGER = True
