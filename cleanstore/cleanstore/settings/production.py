from .base import *

DEBUG = False

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

