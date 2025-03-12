from celery import Celery
from celery.schedules import crontab

from config import config

app = Celery('set_groups_celery',
             broker=config.REDIS_URL + str(config.CELERY_BROKER_DB),
             backend=config.REDIS_URL + str(config.CELERY_BACKEND_DB),
             include=['get_groups.tasks'])

app.conf.beat_schedule = {
    'create_set_groups_task': {
        'task': 'get_groups.tasks.create_set_groups_task',
        'schedule': crontab(minute=0, hour=0),
        'args': []
    },
}
