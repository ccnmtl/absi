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
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': os.environ.get('DATABASE_HOST'),
            'PORT': os.environ.get('DATABASE_PORT'),
        }
    }

MIDDLEWARE += [  # noqa
    'django.middleware.csrf.CsrfViewMiddleware',
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
REDIS_HOST = 'localhost'
if os.environ.get('REDIS_HOST'):
    REDIS_HOST = os.environ.get('REDIS_HOST')

REDIS_PORT = 6379
if os.environ.get('REDIS_PORT'):
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
            'prefix': project + ':asgi',
        },
    },
}
