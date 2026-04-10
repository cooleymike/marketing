import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EP.settings')

app = Celery('EP')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()