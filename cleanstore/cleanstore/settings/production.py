from .base import *
import dj_database_url

DEBUG = False
i
DATABASES = {
    'default': dj_database_url.config(default='postgres://ken:invincible@db:5432/staples')
}
