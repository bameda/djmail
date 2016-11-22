from django.apps import AppConfig


class DjMailConfig(AppConfig):
    name = 'djmail'
    verbose_name = "DjMail"

    def ready(self):
        from . import signals
        super(DjMailConfig, self).ready()
