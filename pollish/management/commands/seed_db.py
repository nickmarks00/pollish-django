from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections, connection
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Populates connected database(s) with data'

    def handle(self, *args, **kwargs):
        print('Populating database...')
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'data/master.sql')
        sql = Path(file_path).read_text()
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
        print("Successfully populated remote database...")
