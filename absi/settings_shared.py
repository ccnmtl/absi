# Django settings for absi project.
import os
import os.path
import sys
from ctlsettings.shared import common

project = 'absi'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'absi.main',
]

ASGI_APPLICATION = 'absi.asgi.application'
USE_TZ = True

if 'test' not in sys.argv and 'jenkins' not in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DATABASE_NAME') or project,
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST'),
            'PORT': os.environ.get('DATABASE_PORT'),
            'CONN_MAX_AGE': 60,
            'CONN_HEALTH_CHECKS': True,
        }
    }

MIDDLEWARE += [  # noqa
    'django.middleware.csrf.CsrfViewMiddleware',
]

INSTALLED_APPS = ['daphne'] + INSTALLED_APPS + [  # noqa
    'pagetree',
    'pageblocks',
]

PAGEBLOCKS = [
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'main.PlayBlock',
    'main.ModuleOverviewBlock',
    'main.LetterOverviewBlock',
]

INSTALLED_APPS += [  # noqa
    'django_bootstrap5',
    'django_extensions',
    'markdownify.apps.MarkdownifyConfig',
    's3sign',

    'rest_framework',
    'rest_framework.authtoken',

    'absi.main',
]

ALLOWED_HOSTS += [  # noqa
    '*',
]

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

ACCOUNT_ACTIVATION_DAYS = 7

AWS_REGION = 'us-east-1'

if os.environ.get('AWS_UPLOAD_BUCKET'):
    AWS_UPLOAD_BUCKET = os.environ.get('AWS_UPLOAD_BUCKET')

# Celery
broker_url = 'sqs://'
CELERY_BROKER_URL = broker_url
broker_transport_options = {
    'region': AWS_REGION,
    'queue_name_prefix': 'celery-absi-',
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Redis
REDIS_HOST = '127.0.0.1'
if os.environ.get('REDIS_HOST'):
    REDIS_HOST = os.environ.get('REDIS_HOST')

REDIS_PORT = 6379
if os.environ.get('REDIS_PORT'):
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Redis SSL
REDIS_PROTO = 'rediss'
if REDIS_HOST == '127.0.0.1':
    # non-SSL for local use
    REDIS_PROTO = 'redis'

redis_address = '{}://{}:{}'.format(REDIS_PROTO, REDIS_HOST, REDIS_PORT)
redis_host_obj = {
    'address': f'{redis_address}/0',
}

if REDIS_PROTO == 'rediss':
    redis_host_obj['ssl_cert_reqs'] = None

USE_X_FORWARDED_HOST = True
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [redis_host_obj],
            'prefix': project + ':asgi',
            'serializer_format': 'json',
            'group_expiry': 3600,
            'capacity': 1500,
        },
    },
}

cache_options = {}
if REDIS_PROTO == 'rediss':
    cache_options['ssl_cert_reqs'] = None

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'{redis_address}/1',
        'KEY_PREFIX': f'{project}:cache',
        'OPTIONS': cache_options,
    }
}

# Azure
AZURE_SPEECH_KEY = os.environ.get('AZURE_SPEECH_KEY')
AZURE_SPEECH_ENDPOINT = os.environ.get('AZURE_SPEECH_ENDPOINT')
AZURE_SPEECH_REGION = os.environ.get('AZURE_SPEECH_REGION', 'eastus')

ABSI_LANG = 'ar-SA'
