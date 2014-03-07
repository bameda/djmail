# -*- coding: utf-8 -*-

import threading

from django.conf import settings
from djmail import core

from . import base


def _close_connection_on_finish(function):
    @functools.wraps(function)
    def _decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        finally:
            connection.close()

    return _decorator


class EmailBackend(base.BaseEmailBackend):
    def _send_messages(self, email_messages):
        if len(email_messages) == 0:
            return 0

        send_async = getattr(settings, "DJMAIL_SEND_ASYNC", False)
        if send_async:
            @_close_connection_on_finish
            def _send(messages):
                return core._send_messages(email_messages)

            thread = threading.Thread(target=_send, args=[email_messages])
            thread.start()
            return thread

        return core._send_messages(email_messages)
