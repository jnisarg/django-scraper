import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

app = Celery('scraper')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

# added beat_schedule from admin
app.conf.beat_schedule = {
    # 'scrape_dev_to_everyday_at_00': {
    #     'task': 'core.tasks.scrape_dev_to_task',
    #     'schedule': crontab(hour=(0, 12), minute=0),
    # },
    # 'scrape_hn_at_00': {
    #     'task': 'core.tasks.scrape_hacker_news_task',
    #     'schedule': crontab(hour=2, minute=42),
    # }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return f'Request: {self.request!r}'
