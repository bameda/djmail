# -*- encoding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf import settings

if settings.EMAIL_BACKEND == 'djmail.backends.celery.EmailBackend':
    from .celery import app as celery_app

    __all__ = ['celery_app']
