from django.apps import AppConfig


class DjMailConfig(AppConfig):
    name = 'djmail'
    verbose_name = "DjMail"

    def ready(self):
        from .signals import generate_uuid
        super(DjMailConfig, self).ready()
