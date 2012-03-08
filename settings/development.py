from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sms_report',
        'USER': 'sms_dev',
        'PASSWORD': 'sms_dev',
        'HOST': '',
        'PORT': '',
    }
}