import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

app = Celery('scraper')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    return f'Request: {self.request!r}'
