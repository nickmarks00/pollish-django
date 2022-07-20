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
        
        if settings.DEBUG:
            cursor1 = connections['mysql'].cursor()
            cursor2 = connections['postgres'].cursor()

            try:
                with cursor1 as cursor:
                    cursor1.execute(sql)
                print("Successfully populated default database...")
            except Exception as e:
                print(e)

            try:
                with cursor2 as cursor:
                    cursor2.execute(sql)
                print("Successfully populated postgres database...")
            except Exception as e:
                print(e)
        else:
            with cursor.connection() as cursor:
                cursor.execute(sql)
             print("Successfully populated remote database...")
