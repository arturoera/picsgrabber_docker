# Import some utility functions
from os.path import join
import os
# Fetch our common settings
from common import *

# #########################################################

# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

FB_PAGE_ID = os.environ.get('FB_PAGE_ID', '')
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN', '')
IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID', '')
IMGUR_CLIENT_TOKEN = os.environ.get('IMGUR_CLIENT_TOKEN', '')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2',
                                               # 'mysql','sqlite3' or 'oracle'.
        'NAME': os.environ.get('DB_ENV_DB', 'devdb'),         # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': os.environ.get('DB_ENV_USER', 'devuser'),
        'PASSWORD': os.environ.get('DB_ENV_PASSWORD', 'devpass'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),       # Empty for localhost through domain sockets
                                   # or '127.0.0.1' for localhost through TCP.
        'PORT': os.environ.get('DB_PORT', '3306'),           # Set to empty string for default.
    }
}

# ##### APPLICATION CONFIGURATION #########################

CUSTOM_APPS = [
	'debug_toolbar',
	]

INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS
