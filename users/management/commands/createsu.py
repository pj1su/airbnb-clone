from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates Superuser"

    def handle(self, *arg, **options):
        admin = User.objects.get_or_none(username="jisuadmin")
        if not admin:
            User.objects.create_superuser("jisuadmin", "123@123.com", "123")
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exit"))