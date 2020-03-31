"""distributed task queue
this is used to count pv, uv, vv.
    - pv: page visit
    - uv: user visit
    - vv: online visitors
"""
import os

from celery import Celery

ENVIRON_MODULE = os.environ.get('DJANGO_BACKEND_PROFILE', 'develop')
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'backend.config.settings.%s' % ENVIRON_MODULE
)

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
