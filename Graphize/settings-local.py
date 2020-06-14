from kombu import Queue, Exchange

from Graphize.settings import *

ALLOWED_HOSTS = ['*.localhost', 'localhost', '*']

SERVER_HOST = 'app.localhost'

# session storage
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
USER_AGENTS_CACHE = 'default'


#------------------Celery Settings---------------------
BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://localhost'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERYD_TASK_SOFT_TIME_LIMIT = 18000

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_QUEUES = (
    Queue('default_queue', Exchange('default_queue'), routing_key='default_queue'),
)
#------------------------------------------------------


#-----------------Cache Setting------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 1800,
    }
}
#------------------------------------------------------


#------------------DATABASES---------------------------
# # LOCAL
# BROKER_URL = 'amqp://localhost'
# CELERY_RESULT_BACKEND = 'amqp://localhost'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'graphize',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
#------------------DATABASES---------------------------


# Instantiate Django
import django
django.setup()
