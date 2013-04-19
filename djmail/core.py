# -*- coding: utf-8 -*-

import functools

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import get_connection
from django.db import connection

from . import models

def _close_connection_on_finish(function):
    @functools.wraps(function)
    def _decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        finally:
            connection.close()

    return _decorator


def _get_real_backend():
    real_backend_path = getattr(settings, "DJMAIL_REAL_BACKEND",
                           'django.core.mail.backends.console.EmailBackend')
    return get_connection(backend=real_backend_path, fail_silently=True)


def send_messages(messages):
    _connection = _get_real_backend()

    # Create a messages on a database for correct
    # tracking of their status.
    _messages = [models.Message.from_email_message(email_message, save=True)
                 for email_message in messages]

    # Open connection for send all messages
    _connection.open()
    _sended_counter = 0

    for message_model in _messages:
        _email = message_model.get_email_message()
        _sended = _connection.send_messages([_email])

        if _sended == 1:
            message_model.status = models.STATUS_SENT
            message_model.save()

            _sended_counter += 1
        else:
            message_model.status = models.STATUS_FAILED
            message_model.save()

    _connection.close()
    return _sended_counter
