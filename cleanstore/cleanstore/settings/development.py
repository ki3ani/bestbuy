from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'staples',
        'USER': 'ken',
        'PASSWORD': 'invincible',
        'HOST': 'db',
        'PORT': '5432',
    }
}