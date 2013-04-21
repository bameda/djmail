# -*- coding: utf-8 -*-

import base64
import pickle
import uuid

from django.db import models


STATUS_DRAFT = 0
STATUS_SENT = 1
STATUS_FAILED = 2
STATUS_DISCARTED = 3

PRIORITY_LOW = 20
PRIORITY_STANDARD = 50
PRIORITY_HIGH = 100


class Message(models.Model):
    STATUS_CHOICES = (
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
        (STATUS_DISCARTED, "Discarted"),
    )

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, "Low"),
        (PRIORITY_STANDARD, "Standard"),
        (PRIORITY_HIGH, "High")
    )

    uuid = models.CharField(max_length=40, primary_key=True,
                            default=lambda: str(uuid.uuid1()))

    data = models.TextField(blank=True)
    retry_count = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=PRIORITY_STANDARD)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, default=None)

    def get_email_message(self):
        raw_pickle_data = base64.decodestring(self.data)
        return pickle.loads(raw_pickle_data)

    @classmethod
    def from_email_message(cls, email_message, save=False):
        data = base64.encodestring(pickle.dumps(email_message))
        instance = cls(data=data)

        if save:
            instance.save()

        return instance
