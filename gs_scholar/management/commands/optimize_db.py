from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Optimize SQLite database'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            self.stdout.write("Running VACUUM...")
            cursor.execute('VACUUM')
            self.stdout.write("VACUUM completed.")
            
            self.stdout.write("Running ANALYZE...")
            cursor.execute('ANALYZE')
            self.stdout.write("ANALYZE completed.")
