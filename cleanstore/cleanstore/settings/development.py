from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'staples',
        'USER': 'ken',
        'PASSWORD': 'invincible',
        'HOST': 'localhost',  # This should match the service name in docker-compose.yml
        'PORT': '5432',
    }
}