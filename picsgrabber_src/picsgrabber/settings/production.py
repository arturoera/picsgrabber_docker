# for now fetch the development settings only
from dev import *

PRODUCTION_APPS = [
	'webapp',
]

INSTALLED_APPS = INSTALLED_APPS + PRODUCTION_APPS