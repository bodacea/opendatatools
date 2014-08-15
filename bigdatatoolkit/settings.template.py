# -*- coding: utf-8 -*-
import os
gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Django settings for bdt project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SERVER_EMAIL = 'sara.farmer@btinternet.com'
ADMINS = (
    ('Sara', 'sara@changeassembly.com'),
    ('Saratoo', 'sara.farmer@btinternet.com'),
)
DEFAULT_FROM_EMAIL = 'sara@changeassembly.com'

MANAGERS = ADMINS

if DEBUG:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'bdt',
			'USER': 'postgres',
			'PASSWORD': 's0meth1ng',
			'HOST': '',
			#'ENGINE': 'django.db.backends.sqlite3',
			#'NAME': os.path.join(PROJECT_PATH, 'database.sqlite'),
			}
		}
else:
	DATABASES = {
		'default': {
			'ENGINE': '@app_engine@',
			'NAME': '@app_name@',
			'USER': '@app_name@',
			'PASSWORD': '@app_pwd@',
			'HOST': '@db_host@',
			'PORT': '@db_port@',
			}
		}
	

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '@app_dir@/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = '@app_dir@/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'latt3sarenice1att354reg00d!w4ntc0ff#$!nthem0rning'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    '@app_dir@/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #'django.contrib.admindocs',
    'cicada',
    #'volta',
)

# Logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '@app_dir@/errors_other.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': '@app_dir@/errors_djrequest.log',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
    'root': {
        'handlers':['default'],
        'level': 'DEBUG',
    },
}
