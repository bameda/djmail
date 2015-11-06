# -*- encoding: utf-8 -*-

from celery.task import task
from django.utils.six import binary_type

from . import core
from . import utils


@task(name="tasks.send_messages")
def send_messages(messages):
    """
    Celery standard task for send async messages.
    """
    return core._send_messages([
        utils.deserialize_email_message(m)
        if isinstance(m, binary_type) else m
        for m in messages
    ])


@task(name="tasks.retry_send_messages")
def retry_send_messages():
    """
    Celery periodic task for retry send failed messages.
    """
    core._send_pending_messages()
    core._mark_discarded_messages()
    core._retry_send_messages()
