import os
from datetime import timedelta

from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover

app = Celery('simplechat')


class CeleryAppConfig(AppConfig):
    name = 'simplechat.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.
        app.config_from_object('django.conf:settings', namespace='CELERY')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration
            # Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            # @formatter:off
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal as raven_register_signal
            from raven.contrib.celery import register_logger_signal as raven_register_logger_signal
            # @formatter:on

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['dsn'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)


app.conf.beat_schedule = {
    'stats-every-10-seconds': {
        'task': 'simplechat.main.tasks.send_user_stats',
        'schedule': timedelta(seconds=10),
    },
}

app.conf.update(
    worker_pool_restarts=True
)
