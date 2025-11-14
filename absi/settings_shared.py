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

INSTALLED_APPS += [  # noqa
    'django_bootstrap5',
    'django_extensions',
    'markdownify.apps.MarkdownifyConfig',

    'absi.main',
]

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

ACCOUNT_ACTIVATION_DAYS = 7
