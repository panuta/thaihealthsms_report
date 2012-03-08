from settings import *

WEBSITE_DOMAIN = 'localhost:8000'

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@thaihealthsms.mailgun.org'
EMAIL_HOST_PASSWORD = '0nvpm5iis068'
EMAIL_PORT = 587

SYSTEM_NOREPLY_EMAIL = 'noreply@thaihealthsms.mailgun.org'