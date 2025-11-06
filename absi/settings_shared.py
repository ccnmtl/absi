# Django settings for absi project.
import os.path
from ctlsettings.shared import common

project = 'absi'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'absi.main',
]

USE_TZ = True

if DEBUG:  # noqa
    INSTALLED_APPS += [  # noqa
        'debug_toolbar',
    ]
    MIDDLEWARE += [  # noqa
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

INSTALLED_APPS += [  # noqa
    'django_bootstrap5',
    'django_extensions',
    'markdownify.apps.MarkdownifyConfig',

    'absi.main',
]

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

ACCOUNT_ACTIVATION_DAYS = 7
