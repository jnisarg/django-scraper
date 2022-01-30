import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write(self.style.WARNING(
                    "Database connection failed. Waiting 1 second before retrying..."))
                time.sleep(1.0)

        self.stdout.write(self.style.SUCCESS("Database available!"))
