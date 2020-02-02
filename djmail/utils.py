import base64
import pickle

from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

__all__ = ('force_bytes', 'force_str',
           'deserialize_email_message', 'serialize_email_message')


def deserialize_email_message(data):
    return pickle.loads(base64.b64decode(force_bytes(data)))


def serialize_email_message(email_message):
    return force_str(base64.b64encode(pickle.dumps(email_message)))
