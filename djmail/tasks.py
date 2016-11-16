# -*- encoding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from . import core
from . import utils

from celery import Celery

app = Celery('djmail')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


@shared_task
def send_messages(messages):
    """
    Celery standard task for sending messages asynchronously.
    """
    return core._send_messages([
        utils.deserialize_email_message(m)
        if isinstance(m, utils.string_types) else m
        for m in messages
    ])


@shared_task
def retry_send_messages():
    """
    Celery periodic task retrying to send failed messages.
    """
    core._send_pending_messages()
    core._mark_discarded_messages()
    core._retry_send_messages()
