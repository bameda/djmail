# -*- encoding: utf-8 -*-

from djmail import core

from . import base


class EmailBackend(base.BaseEmailBackend):
    def _send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        return core._send_messages(email_messages)
