import os
from absi.settings_shared import *  # noqa: F401,F403
from ctlsettings.production import common, init_sentry


locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        s3static=True,
    ))


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


ALLOWED_HOSTS += [  # noqa
    '*',
]


try:
    from absi.local_settings import *  # noqa: F403, F401
except ImportError:
    pass


SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    init_sentry(SENTRY_DSN)
