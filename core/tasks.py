from celery import shared_task

from .scrapers import scrape_dev_to, scrape_hn


@shared_task(bind=True)
def scrape_dev_to_task(self):
    scrape_dev_to(url="https://dev.to/latest")
    return "Done"


@shared_task(bind=True)
def scrape_hacker_news_task(self, crawl_delay=30):
    scrape_hn(crawl_delay=crawl_delay)
    return "Done"
