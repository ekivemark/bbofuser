"""
Django settings for developeraccount project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from platform import python_version
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# The real value is set in the local_settings.py
# local_settings.py is excluded from the git repository
# Place other important keys, passwords etc. in local_settings.py
# which is called at the end of settings.py

# I recommend setting a default/false value in settings.py
# and then overwriting in local_settings. This keeps the app
# functional if anyone clones the repository
# You can generate a new SECRET_KEY using tools such as
# http://www.miniwebtool.com/django-secret-key-generator/
#
SECRET_KEY = 'FAKE_VALUE_REAL_VALUE_SET_IN_LOCAL_SETTINGS'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

DEBUG_SETTINGS = True

ALLOWED_HOSTS = []
ADMINS = (
     ('Mark Scrimshire', 'mark@ekivemark.com'),
)

MANAGERS = ADMINS

APPLICATION_TITLE = "BB+ Developer Accounts"

if DEBUG_SETTINGS:
    print "Application: %s" % APPLICATION_TITLE
    print "Running on Python_version: %s" % python_version()
    print ""
    print "BASE_DIR:%s " % BASE_DIR

# Application definition

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
   )


DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    # add django.contrib.sites to support django registration
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    # Add third party libraries here
    'mongoengine',
    'bootstrap3',
    'bootstrapform',
    'registration',
)

LOCAL_APPS = (
    # Add custom apps here
    'apps.developer',

)


INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'developeraccount.urls'

WSGI_APPLICATION = 'developeraccount.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DBPATH = os.path.join(BASE_DIR, 'db/db.db')
if DEBUG_SETTINGS:
    print "DBPATH:",DBPATH


# Standard sqlite3 settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DBPATH,                  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
# Plan on sqlite3 for development environment
# Use Postgreql for Production

# Use SQL platform for user and session management
# Use MongoDb for documents

#Mongo DB settings
# MONGO_HOST = "127.0.0.1"
MONGO_HOST = "172.31.13.249"
MONGO_PORT = 27017
MONGO_DB_NAME = "BlueButtonRepository"
MONGO_ALIAS = "default"
MONGO_MASTER_COLLECTION = "main"
MONGO_HISTORYDB_NAME = "history"
MONGO_LIMIT = 100
MONGO_USER = ""
MONGO_PASSWORD = ""

from mongoengine import connect
# MONGO_CONNECTION = connect(MONGO_DB_NAME,
#                            alias=MONGO_ALIAS,
#                            username=MONGO_USER, password=MONGO_PASSWORD,
#                            host=MONGO_HOST, port=MONGO_PORT,
#                            )
# if DEBUG_SETTINGS:
#     print "MONGO_CONNECTION:",MONGO_CONNECTION


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



STATIC_URL = '/static/'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    # This should always be the last in the list because it is our default.
    os.path.join(BASE_DIR, 'templates'),

)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# For Django Registration:
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = False # Automatically log the user in.

# Django Registration
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# to use console open terminal and run:
# python -m smtpd -n -c DebuggingServer localhost:1025
# Replacing localhost:1025 with EMAIL_HOST:EMAIL_PORT if different
DEFAULT_FROM_EMAIL = 'accounts@dev.bbonfhir.com'

if DEBUG_SETTINGS:
    print "Email via %s" % EMAIL_BACKEND
    print "Email Host:Port: %s:%s" % (EMAIL_HOST, EMAIL_PORT)

# Django 1.6+ implement a new test runner
# Suppress error 1_6.W001 by adding:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Get Local Settings that you want to keep private.
# Make sure Local_settings.py is excluded from Git
try:
    from developeraccount.local_settings import *
except Exception as e:
    print "ERROR: local_settings not loaded"
    pass

if DEBUG_SETTINGS:
    print "SECRET_KEY:%s" % SECRET_KEY
    print "================================================================"
# SECURITY WARNING: keep the secret key used in production secret!

