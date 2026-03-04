from django.core.management.base import BaseCommand
from mailing.services import run_mailings

class Command(BaseCommand):
    help = 'Runs all scheduled mailings'

    def handle(self, *args, **options):
        self.stdout.write('Checking and running mailings...')
        run_mailings()
        self.stdout.write(self.style.SUCCESS('Successfully completed mailing run'))
