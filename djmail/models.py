# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import base64
import pickle
import uuid

try:
    # Django >= 1.4.5
    from django.utils.encoding import force_bytes, force_text
except ImportError:
    # Django < 1.4.5
    from django.utils.encoding import (
        smart_unicode as force_text, smart_str as force_bytes)
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_save


STATUS_DRAFT = 10
STATUS_PENDING = 20
STATUS_SENT = 30
STATUS_FAILED = 40
STATUS_DISCARDED = 50

PRIORITY_LOW = 20
PRIORITY_STANDARD = 50


class Message(models.Model):
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
        (STATUS_DISCARDED, "Discarded"),
    )

    uuid = models.CharField(max_length=40, primary_key=True)

    from_email = models.CharField(max_length=1024, blank=True)
    to_email = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    body_html = models.TextField(blank=True)
    subject = models.CharField(max_length=1024, blank=True)

    data = models.TextField(blank=True, editable=False)

    retry_count = models.SmallIntegerField(default=-1)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)
    priority = models.SmallIntegerField(default=PRIORITY_STANDARD)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, default=None)
    exception = models.TextField(editable=True, blank=True)

    def get_email_message(self):
        raw_pickle_data = base64.b64decode(force_bytes(self.data))
        return pickle.loads(raw_pickle_data)

    @classmethod
    def from_email_message(cls, email_message, save=False):
        def get_body_key(the_type):
            """Declare HTML body subtype as text/html else as text/plain."""
            return 'body_' + ('html' if the_type.split('/')[-1] == 'html' else 'text')

        kwargs = {
            'from_email': force_text(email_message.from_email),
            'to_email': ','.join(force_text(x) for x in email_message.to),
            get_body_key(email_message.content_subtype): force_text(email_message.body),
            'subject': force_text(email_message.subject),
            'data': base64.b64encode(pickle.dumps(email_message))
        }

        # Update the body (if missing) from the alternatives
        for content, the_type in getattr(email_message, 'alternatives', None) or []:
            kwargs.setdefault(get_body_key(the_type), content)

        instance = cls(**kwargs)
        if save:
            instance.save()

        return instance

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"


@receiver(pre_save, sender=Message, dispatch_uid='message_uuid_signal')
def generate_uuid(sender, instance, **kwargs):
    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())
