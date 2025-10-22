from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_retry = True
app.conf.broker_connection_max_retries = 0

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

__all__ = ('app',)