import os
import time

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks()  # Чтобы celery автоматически смотрела по всем папкам и искала таски

app.conf.beat_schedule = {
    'calculation_bookmark_rating_votes_every_3_hour':
        {
            'task': 'api.v1.composition.tasks.calculate_bookmarks_ratings_votes',
            # 'schedule': crontab(minute='*/1'),
            'schedule': crontab(minute=0, hour='*/3'),
        }
}


@app.task()
def debug_task():
    time.sleep(20)
    print('Hello from debug_task')
