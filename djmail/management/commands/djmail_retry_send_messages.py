# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from ... import core


class Command(BaseCommand):
    def handle(self, *args, **options):
        core._send_pending_messages()
        core._mark_discarded_messages()
        core._retry_send_messages()

        return 0
