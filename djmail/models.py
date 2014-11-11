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


STATUS_DRAFT = 10
STATUS_PENDING = 20
STATUS_SENT = 30
STATUS_FAILED = 40
STATUS_DISCARDED = 50

PRIORITY_LOW = 20
PRIORITY_STANDARD = 50

def new_uuid():
    return str(uuid.uuid1())

class Message(models.Model):
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
        (STATUS_DISCARDED, "Discarded"),
    )

    uuid = models.CharField(max_length=40, primary_key=True,
                            default=new_uuid())

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
        kwargs = {
            "from_email": force_text(email_message.from_email),
            "to_email": ",".join(force_text(x) for x in email_message.to),
            "body_text": force_text(email_message.body),
            "subject": force_text(email_message.subject),
            "data": base64.b64encode(pickle.dumps(email_message)),
        }

        if hasattr(email_message, "alternatives") and len(email_message.alternatives) > 0:
            html_alts = [x[0] for x in email_message.alternatives if x[1] == "text/html"]
            kwargs["body_html"] = html_alts[0] if len(html_alts) > 0 else ""

        instance = cls(**kwargs)
        if save:
            instance.save()

        return instance

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"
