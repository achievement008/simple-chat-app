from django.apps import AppConfig

from simplechat.main.user_store import UserConnections


class MainConfig(AppConfig):
    name = "simplechat.main"
    verbose_name = "Чат"

    def ready(self):
        UserConnections.init()
