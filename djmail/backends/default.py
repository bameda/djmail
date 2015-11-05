# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from djmail import core

from . import base


class EmailBackend(base.BaseEmailBackend):
    """
    Default email back-end that sends e-mails
    synchronously.
    """
    def send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        return core._send_messages(email_messages)
