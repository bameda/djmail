# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from . import base
from .. import tasks


class EmailBackend(base.BaseEmailBackend):
    """
    Asynchronous email back-end that uses
    Celery task for sending emails.
    """
    def send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        return tasks.send_messages.delay(email_messages)
