from celery import shared_task

from .scrapers import scrape_dev_to


@shared_task(bind=True)
def scrape(self, url):
    scrape_dev_to(url)
    return "Done"
