# flake8: noqa
from absi.settings_shared import *

try:
    from absi.local_settings import *
except ImportError:
    pass
