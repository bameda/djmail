import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Message


@receiver(pre_save, sender=Message, dispatch_uid='message_uuid_signal')
def generate_uuid(sender, instance, **kwargs):
    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())
