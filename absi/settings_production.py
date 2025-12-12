import os
from absi.settings_shared import *  # noqa: F403
from ctlsettings.production import common, init_sentry


locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        # if you use cloudfront:
        #        cloudfront="justtheidhere",
        # if you don't use S3/cloudfront at all:
        #       s3static=False,
    ))


try:
    from absi.local_settings import *  # noqa: F403, F401
except ImportError:
    pass


SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    init_sentry(SENTRY_DSN)
