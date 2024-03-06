from .base import *
import os

DEBUG = False

# Database configuration remains the same
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cleanstore',
        'USER': 'cleanstore_user',
        'PASSWORD': 'ljBHs2QGlIjLwK1VVqQRtDajkVlXjnV9',
        'HOST': 'dpg-cnk1g6821fec73e6phq0-a',  # Use the FQDN or IP address provided by Render
        'PORT': '5432',  # Default PostgreSQL port
    }
}


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
