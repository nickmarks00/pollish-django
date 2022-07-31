import os
import dj_database_url
from decouple import config
from .common import *

DEBUG = False

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

DATABASES = {"default": dj_database_url.config()}


WSGI_APPLICATION = "pollish_dj.wsgi.application"


# SMTP and Emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# # EMAIL_HOST_USER = config('HOST_EMAIL')
# # EMAIL_HOST_PASSWORD = config('HOST_EMAIL_PASSWORD')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True


# Amazon S3 Buckets Config
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "pollishorg-media-bucket"

# from django-storages
AWS_S3_FILE_OVERWRITE = False  # defaults to True
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Auto upload static files to bucket
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

AWS_S3_HOST = "s3.ap-southeast-2.amazonaws.com"
AWS_S3_REGION_NAME = "ap-southeast-2"
