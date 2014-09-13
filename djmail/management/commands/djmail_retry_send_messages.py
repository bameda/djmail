# -*- encoding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from djmail import core


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        core._send_pending_messages()
        core._mark_discarded_messages()
        core._retry_send_messages()

        return 0
