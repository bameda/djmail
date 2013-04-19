# -*- coding: utf-8 -*-

from celery.task import task
from . import core

@task(name="tasks.send_messages")
def send_mail(messages):
    return core.send_messages(messages)
