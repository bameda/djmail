# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import base64
import pickle

from django.utils.encoding import force_bytes


def deserialize_email_message(data):
    return pickle.loads(base64.b64decode(force_bytes(data)))


def serialize_email_message(email_message):
    return base64.b64encode(pickle.dumps(email_message))
