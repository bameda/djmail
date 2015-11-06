# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from django.conf import settings

from djmail.backends import base
from djmail import tasks
from .. import utils


class EmailBackend(base.BaseEmailBackend):
    """
    djmail backend that uses celery task for
    send emails.
    """
    def _send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        if settings.CELERY_TASK_SERIALIZER in ('json', ):
            email_messages = [utils.serialize_email_message(e) for e in email_messages]
        return tasks.send_messages.delay(email_messages)
