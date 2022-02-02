import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

app = Celery('scraper')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'scrape_dev_to_every_12_hours': {
        'task': 'core.tasks.scrape_dev_to_task',
        'schedule': crontab(minute=0, hour='*/12'),
    },
    'scrape_hn_every_12_hours': {
        'task': 'core.tasks.scrape_hacker_news_task',
        'schedule': crontab(minute=0, hour='*/12'),
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return f'Request: {self.request!r}'
