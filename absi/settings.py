# flake8: noqa
from absi.settings_shared import *
from kombu.utils.url import safequote
from django.conf import settings

try:
    from absi.local_settings import *
except ImportError:
    pass


if hasattr(settings, 'AWS_ACCESS_KEY') and hasattr(settings, 'AWS_SECRET_KEY'):
    aws_access_key = safequote(AWS_ACCESS_KEY)
    aws_secret_key = safequote(AWS_SECRET_KEY)
    broker_url = 'sqs://{aws_access_key}:{aws_secret_key}@'.format(
        aws_access_key=aws_access_key, aws_secret_key=aws_secret_key
    )
