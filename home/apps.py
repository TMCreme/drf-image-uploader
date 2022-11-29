from urllib import request
from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_save


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from . import signals
        post_save.connect(signals.create_thumbnail)
