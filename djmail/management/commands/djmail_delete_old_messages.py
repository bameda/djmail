# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from djmail import models


class Command(BaseCommand):
    help = 'Remove (succesfully sent) messages older than specified amount of days.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=183, # default = 6 months
            help='Number of days to use as cut-off for deletion',
        )

    def handle(self, *args, **options):
        models.Message.objects.filter(sent_at__lt=datetime.now() - timedelta(days=options['days']), status=models.STATUS_SENT).delete()
