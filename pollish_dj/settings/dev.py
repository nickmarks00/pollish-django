from .common import *
from decouple import config


DEBUG = True

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pollish', # name of db in mysql / datagrip
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': config('MYSQL_ROOT')
    }
}

