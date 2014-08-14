# -*- encoding: utf-8 -*-

from django.core.mail.backends.locmem import EmailBackend as BaseEmailBackend


class BrokenEmailBackend(BaseEmailBackend):
    def send_messages(self, messages):
        return 0
