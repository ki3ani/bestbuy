from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'staples'),  
        'USER': os.getenv('POSTGRES_USER', 'ken'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'invincible'),
        'HOST': os.getenv('DATABASE_HOST', 'db'), 
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}