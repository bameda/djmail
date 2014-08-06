# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from djmail.backends import base
from djmail import tasks


class EmailBackend(base.BaseEmailBackend):
    """
    djmail backend that uses celery task for
    send emails.
    """
    def _send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        return tasks.send_messages.delay(email_messages)
