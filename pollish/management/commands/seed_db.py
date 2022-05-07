from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Populates connected MySQL client with data'

    def handle(self, *args, **kwargs):
        print('Populating database...')
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'data/master.sql')
        sql = Path(file_path).read_text()

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            print("Successfully populated...")
        except Exception as e:
            print(e)