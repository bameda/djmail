# -*- encoding: utf-8 -*-

from celery.task import task
from . import core


@task(name="tasks.send_messages")
def send_messages(messages):
    """
    Celery standard task for send async messages.
    """
    return core._send_messages(messages)


@task(name="tasks.retry_send_messages")
def retry_send_messages():
    """
    Celery periodic task for retry send failed messages.
    """
    core._send_pending_messages()
    core._mark_discarded_messages()
    core._retry_send_messages()
