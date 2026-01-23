from absi.settings_shared import *  # noqa: F403, F401

try:
    from absi.local_settings import *  # noqa: F403, F401
except ImportError:
    pass
