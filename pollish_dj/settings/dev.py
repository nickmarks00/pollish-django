from .common import *
from decouple import config
import os


DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,').split(',')

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pollish', # name of db in mysql / datagrip
        'HOST': 'localhost',
        'USER': 'pollish',
        'PASSWORD': config('POSTGRES_PWD', default='localhost'),
        'PORT': '',
    }
}

default_database = os.environ.get('DJANGO_DATABASE', 'postgres')
DATABASES['default'] = DATABASES[default_database]


# SMTP and Emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_USER = ''
# EMAIL_PASSWORD = ''
# EMAIL_PORT = 2525
# DEFAULT_FROM_MAIL = 'pollish.org@gmail.com'

