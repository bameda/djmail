# -*- coding: utf-8 -*-

import threading

from django.conf import settings
from djmail.backends import base
from djmail import core


class EmailBackend(base.BaseEmailBackend):
    def _load_settings(self):
        self._send_async = getattr(settings, "DJMAIL_SEND_ASYNC", False)

    def _send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        self._load_settings()

        if self._send_async:
            @core._close_connection_on_finish
            def _send(messages):
                return core._send_messages(email_messages)

            thread = threading.Thread(target=_send, args=[email_messages])
            thread.start()
            return thread

        return core._send_messages(email_messages)
