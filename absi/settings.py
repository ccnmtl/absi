import os
from absi.settings_shared import *  # noqa: F403, F401
from kombu.utils.url import safequote

try:
    from absi.local_settings import *  # noqa: F403, F401
except ImportError:
    pass


if os.environ.get('AWS_ACCESS_KEY') and os.environ.get('AWS_SECRET_KEY'):
    aws_access_key = safequote(os.environ.get('AWS_ACCESS_KEY'))
    aws_secret_key = safequote(os.environ.get('AWS_SECRET_KEY'))
    broker_url = 'sqs://{aws_access_key}:{aws_secret_key}@'.format(
        aws_access_key=aws_access_key, aws_secret_key=aws_secret_key
    )
    CELERY_BROKER_URL = broker_url
