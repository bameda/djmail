import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'p23jof024jf5-94j3f023jf230=fj234fp34fijo'

DEBUG = True
ALLOWED_HOSTS = []

# docker run -d -p 5432:5432 -v /var/lib/postgresql postgres
DATABASES = {}
DATABASES['default'] = dj_database_url.config(default='postgres://postgres@localhost:5432/postgres')


# Application definition

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
