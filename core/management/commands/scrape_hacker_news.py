from django.core.management.base import BaseCommand

from core.tasks import scrape_hacker_news_task


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--crawl_delay", nargs="+", type=int, default=30)

    def handle(self, *args, **options):
        crawl_delay = options.get("crawl_delay")
        self.stdout.write("Sending scraping task to celery...")
        scrape_hacker_news_task.delay(crawl_delay=crawl_delay)
        return "Done"
