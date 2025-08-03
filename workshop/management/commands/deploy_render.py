from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run migrations and collect static files for deployment'

    def handle(self, *args, **options):
        self.stdout.write('Running database migrations...')
        call_command('migrate', verbosity=1)
        
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', verbosity=1)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully completed deployment tasks!')
        )
