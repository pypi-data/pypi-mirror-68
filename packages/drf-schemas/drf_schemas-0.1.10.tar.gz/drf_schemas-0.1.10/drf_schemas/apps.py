from django.apps import AppConfig


class DrfSchemasConfig(AppConfig):
    name = 'drf_schemas'

    def ready(self):
        from . import signals
