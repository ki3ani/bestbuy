from .base import *
import os

DEBUG = True

# Database configuration remains the same
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cleanstore',
        'USER': 'cleanstore_user',
        'PASSWORD': 'ljBHs2QGlIjLwK1VVqQRtDajkVlXjnV9',
        'HOST': 'dpg-cnk1g6821fec73e6phq0-a',
        'PORT': '5432', 
    }
}


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
