# -*- encoding: utf-8 -*-


class BaseEmailBackend(object):
    """
    Base class that implements a django
    mail backend interface.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def open(self):
        pass

    def close(self):
        pass

    def _send_messages(self, email_messages):
        raise NotImplementedError

    def send_messages(self, email_messages):
        return self._send_messages(email_messages)
