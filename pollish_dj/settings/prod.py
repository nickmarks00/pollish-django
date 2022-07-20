import os
import dj_database_url
from decouple import config
from .common import *

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': dj_database_url.config()
}


WSGI_APPLICATION = 'pollish_dj.wsgi.application'



# SMTP and Emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# # EMAIL_HOST_USER = config('HOST_EMAIL')
# # EMAIL_HOST_PASSWORD = config('HOST_EMAIL_PASSWORD')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True