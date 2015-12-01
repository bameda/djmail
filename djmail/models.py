# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_save

from . import utils

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
        return utils.deserialize_email_message(self.data)

    @classmethod
    def from_email_message(cls, email_message, save=False):
        kwargs = {
            "from_email": utils.force_text(email_message.from_email),
            "to_email": ",".join(utils.force_text(x) for x in email_message.to),
            "subject": utils.force_text(email_message.subject),
            "data": utils.serialize_email_message(email_message),
        }

        if email_message.content_subtype.endswith("plain"):
            kwargs["body_text"] = utils.force_text(email_message.body)
        elif email_message.content_subtype.endswith("html"):
            kwargs["body_html"] = utils.force_text(email_message.body)

        try:
            alt_body, alt_type = email_message.alternatives[0]
            if not kwargs.get("body_text") and alt_type.endswith("plain"):
                kwargs["body_text"] = utils.force_text(alt_body)
            elif not kwargs.get("body_html") and alt_type.endswith("html"):
                kwargs["body_html"] = utils.force_text(alt_body)
        except (AttributeError, IndexError):
            pass

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
