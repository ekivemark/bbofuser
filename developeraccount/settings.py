"""
Django settings for developeraccount project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from ConfigParser import RawConfigParser
parser = RawConfigParser()
# http://stackoverflow.com/questions/4909958/django-local-settings/14545196#14545196


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from platform import python_version
from util import str2bool, str2int


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

APPLICATION_ROOT = BASE_DIR

# Config file should be installed in parent directory
# format is:
# [global]
# domain = dev.bbonfhir.com
# debug = True
# template_debug = True
# debug_settings = True
# email_host = box905.bluehost.com
#

CONFIG_FILE = 'local.ini'
# Read the config file
parser.readfp(open(os.path.join(APPLICATION_ROOT, CONFIG_FILE)))
# Then use parser.get(SECTION, VARIABLE) to read in value
# Value is in string format
# Use util functions to convert strings to boolean or Integer


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

SECRET_KEY = 'FAKE_VALUE_REAL_VALUE_SET_FROM_..LOCAL.INI'
SECRET_KEY = parser.get('global', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str2bool(parser.get('global', 'debug'))

TEMPLATE_DEBUG = str2bool(parser.get('global', 'template_debug'))

DEBUG_SETTINGS = str2bool(parser.get('global', 'debug_settings'))

ALLOWED_HOSTS = []
ADMINS = (
     ('Mark Scrimshire', 'mark@ekivemark.com'),
)

MANAGERS = ADMINS

APPLICATION_TITLE = "BB+ Developer Accounts"
APPLICATION_TITLE = parser.get('global', 'application_title')


if DEBUG_SETTINGS:
    print "Application: %s" % APPLICATION_TITLE
    print "Running on Python_version: %s" % python_version()
    print ""
    print "BASE_DIR:%s " % BASE_DIR
    print "APPLICATION_ROOT:%s " % APPLICATION_ROOT
    FULL_CONFIG_FILE = APPLICATION_ROOT.strip()+'/'+CONFIG_FILE
    print "Config File: %s" % FULL_CONFIG_FILE

# Application definition

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
   )


DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    # add django.contrib.auth to support django registration
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
    # 'mongoengine',
    'bootstrap3',
    'bootstrapform',
    # this installs django-registration-redux
    'registration',
    'oauth2_provider',
    'corsheaders',

)

LOCAL_APPS = (
    # Add custom apps here
    'accounts',

)


INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL= "accounts.User"
USERNAME_FIELD = "email"
#AUTHENTICATION_BACKENDS = ['accounts.backends.EmailAuthBackend',]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
# MONGO_HOST = "172.31.13.249"
# MONGO_PORT = 27017
# MONGO_DB_NAME = "BlueButtonRepository"
# MONGO_ALIAS = "default"
# MONGO_MASTER_COLLECTION = "main"
# MONGO_HISTORYDB_NAME = "history"
# MONGO_LIMIT = 100
# MONGO_USER = ""
# MONGO_PASSWORD = ""
#
# from mongoengine import connect
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

# SITE_ID = 1 = prod - dev.bbonfhir.com
# SITE_ID = 2 = local - localhost:8000
SITE_ID = 3
if DEBUG_SETTINGS:
    print "Site_ID: %s" % SITE_ID

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

SESSION_COOKIE_SECURE = False
SESSON_ENGINE = 'django.contrib.sessions.backends.db'

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
# settings are stored in local.ini in parent directory
ACCOUNT_ACTIVATION_DAYS = str2int(parser.get('global', 'account_activation_days'))
try:
    ACCOUNT_ACTIVATION_DAYS = int(ACCOUNT_ACTIVATION_DAYS)
except:
    ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.

REGISTRATION_AUTO_LOGIN = False # Automatically log the user in.
REGISTRATION_AUTO_LOGIN = str2bool(parser.get('global', 'registration_auto_login'))

#REGISTRATION_FORM = 'accounts.admin.UserCreationForm'

# Django Registration
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST = parser.get('global', 'email_host').strip()
# EMAIL_PORT = 1025 # local
EMAIL_PORT = 645 # SSL
EMAIL_PORT = str2int(parser.get('global', 'email_port'))


EMAIL_HOST_USER = parser.get('global','email_host_user')
EMAIL_HOST_PASSWORD = parser.get('global','email_host_password')

#EMAIL_USE_TLS = True
# Port 465 = SSL
# Port 587 = TLS
EMAIL_USE_SSL = True
EMAIL_USE_SSL = str2bool(parser.get('global', 'email_use_ssl'))

EMAIL_BACKEND_TYPE = parser.get('global', 'email_backend_type')
if EMAIL_BACKEND_TYPE == 'smtp':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/'

# SMS code Time out in Minutes (used for Multi-factor Authentication
SMS_LOGIN_TIMEOUT_MIN = 5



# to use console open terminal and run:
# python -m smtpd -n -c DebuggingServer localhost:1025
# Replacing localhost:1025 with EMAIL_HOST:EMAIL_PORT if different
DEFAULT_FROM_EMAIL = parser.get('global', 'default_from_email')

if DEBUG_SETTINGS:
    print "Email via %s: %s" % (EMAIL_BACKEND_TYPE, EMAIL_BACKEND)
    print "Account Activation Days: %s" % ACCOUNT_ACTIVATION_DAYS
    print "Email Host:Port: %s:%s" % (EMAIL_HOST, EMAIL_PORT)
    print "Credentials: [%s]/[%s]" % (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

# END of DJANGO Registration Settings Section

# CORSHEADERS Configuration
# Set ALLOW_ALL to True for testing only
CORS_ORIGIN_ALLOW_ALL = True

# End of CORSHEADERS Section
# Change to OAuth2 Provider Application Model
#OAUTH2_PROVIDER_APPLICATION_MODEL='accounts.MyApplication'


# Django 1.6+ implement a new test runner
# Suppress error 1_6.W001 by adding:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Get Local Settings that you want to keep private.
# Make sure Local_settings.py is excluded from Git
# try:
#     from developeraccount.local_settings import *
# except Exception as e:
#     print "ERROR: local_settings not loaded"
#     pass

if DEBUG_SETTINGS:
    print "SECRET_KEY:%s" % SECRET_KEY
    print "================================================================"
# SECURITY WARNING: keep the secret key used in production secret!

