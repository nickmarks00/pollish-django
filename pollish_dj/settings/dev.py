from .common import *
from decouple import config
import os


DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pollish', # name of db in mysql / datagrip
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': config('MYSQL_ROOT'),
        'PORT': '',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pollish', # name of db in mysql / datagrip
        'HOST': 'localhost',
        'USER': 'nickm',
        'PASSWORD': config('POSTGRES_ROOT'),
        'PORT': '',
    }
}

default_database = os.environ.get('DJANGO_DATABASE', 'mysql')
DATABASES['default'] = DATABASES[default_database]


# SMTP and Emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_USER = ''
# EMAIL_PASSWORD = ''
# EMAIL_PORT = 2525
# DEFAULT_FROM_MAIL = 'pollish.org@gmail.com'

