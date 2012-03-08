# -*- encoding: utf-8 -*-

import os
base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir) 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

WEBSITE_NAME = 'Thai Health SMS'
WEBSITE_DOMAIN = 'localhost:8000'

ADMINS = (
    ('Panu Tangchalermkul', 'panuta@gmail.com'),
)

MANAGERS = ADMINS

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

TIME_ZONE = 'Asia/Bangkok'
LANGUAGE_CODE = 'th'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(base_path, 'media/')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(base_path, 'sitestatic/')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(base_path, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'application.testbed@gmail.com'
EMAIL_HOST_PASSWORD = 'opendream'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = 'Thai Health Report - '

""" MailGun Email Service
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@thaihealthsms.mailgun.org'
EMAIL_HOST_PASSWORD = '0nvpm5iis068'
EMAIL_PORT = 587
"""

""" SENDGRID EMAIL SERVICE
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'sendgrid_username'
EMAIL_HOST_PASSWORD = 'sendgrid_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
"""

SYSTEM_NOREPLY_EMAIL = 'noreply@thaihealthsms.mailgun.org'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'backends.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#)wsx5ovooy57-5(ief^^)!*b4jhc=o#2$+i0$#8m1-@$19m_^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'middleware.AJAXSimpleExceptionResponse',
    'http.Http403Middleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(base_path, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'private_files',

    'accounts',
    'budget',
    'common',
    'domain',
    'management',
    'report',

)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# PRIVATE FILES SETTINGS #

FILE_PROTECTION_METHOD = 'basic'

# THAIHEALTHSMS SETTINGS #

REPORT_ROOT = MEDIA_ROOT + 'report/'
WARNING_AT_DAYS_BEFORE_DUE = 3
