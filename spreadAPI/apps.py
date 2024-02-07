from django.apps import AppConfig
from django.conf import settings


class SpreadapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spreadAPI'

    def ready(self):
        print("AAAAA")
        print(settings.COMMAND)
        if settings.COMMAND == ["runserver"] or settings.COMMAND == ["--bind"]:
            from spreadAPI.management.commands.updateSpreads import Command
            Command().handle(scheduler = "background")
