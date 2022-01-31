from django.core.management.base import BaseCommand

from core.tasks import scrape_dev_to_task


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Sending scraping task to celery...")
        scrape_dev_to_task.delay()
        return "Done"
