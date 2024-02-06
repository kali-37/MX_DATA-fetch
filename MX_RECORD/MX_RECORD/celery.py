

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MX_RECORD.settings')

app = Celery('MX_RECORD')

# Load task modules from all registered Django app configs.

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'fetch and store in db using API': {
        'task': 'myapp.tasks.fetch_and_store_data',
        'schedule': 2,  # Run every 2 seconds
        'options': {
            'expires': 10,  # Set an expiration time for the task
        }
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
