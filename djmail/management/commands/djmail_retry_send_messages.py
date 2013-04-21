# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand, CommandError
from djmail import core

class Command(NoArgsCommand):
    def handle_noargs(**options):
        core._send_pending_messages()
        core._mark_discarted_messages()
        core._retry_send_messages()

        return 0
