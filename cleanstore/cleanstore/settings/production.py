from .base import *
import os

DEBUG = False

# Database configuration remains the same
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


