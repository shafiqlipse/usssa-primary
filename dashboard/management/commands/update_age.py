from django.core.management.base import BaseCommand
from datetime import date
from ...models import Athlete


class Command(BaseCommand):
    help = "Deactivate athletes older than a certain age"

    def handle(self, *args, **kwargs):
        today = date.today()
        min_age = 14

        # Calculate the cutoff date for the desired age
        cutoff_date = today.replace(year=today.year - min_age)

        # Update the status of athletes older than the cutoff date
        athletes_to_update = Athlete.objects.filter(date_of_birth__lte=cutoff_date)
        count = athletes_to_update.update(status="Inactive")

        self.stdout.write(f"Successfully deactivated {count} athletes.")
