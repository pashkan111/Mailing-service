from celery import Celery
import os
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = Celery('service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


CELERY_TASK_IGNORE_RESULT = True
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_IMPORTS = ['dostavisor.common.tasks', 'dostavisor.common.emulator']
CELERY_TASK_ROUTES = {
    'dostavisor.common.tasks.send_message_to_kafka_task': {'queue': 'high'},
}
CELERY_BEAT_SCHEDULE = {
    'preorder-task': {
        'task': 'dostavisor.common.tasks.preorder_task',
        'options': {'queue': 'periodic'},
        'schedule': crontab(minute='*/1'),
    },
}
