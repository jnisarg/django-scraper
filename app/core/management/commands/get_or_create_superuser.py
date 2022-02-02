from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Checking if superuser exists...")
        try:
            admin = User.objects.get(username="admin")
            if admin.is_superuser:
                admin.set_password("admin")
                admin.save()
                self.stdout.write("Superuser found...")
            else:
                admin.delete()
        except User.DoesNotExist:
            admin = User.objects.create_superuser(username="admin", password="admin")
            self.stdout.write("Superuser created...")        
