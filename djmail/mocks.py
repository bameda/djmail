# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core.mail.backends.locmem import EmailBackend as BaseEmailBackend


class BrokenEmailBackend(BaseEmailBackend):
    def send_messages(self, messages):
        return 0
