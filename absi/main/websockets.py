from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging

from absi.main.utils import GROUP_NAME

logger = logging.getLogger(__name__)


def notify_ws(message: str, azure: bool = False):
    """
    Send a JSON-serializable payload to all connected /ws/ clients.
    """
    channel_layer = get_channel_layer()

    if channel_layer is None:
        logger.warning(
            'No channel layer configured; skipping websocket notify')
        return

    try:
        async_to_sync(channel_layer.group_send)(
            GROUP_NAME, {
                'type': 'send_message',
                'message': message,
                'azure': azure,
            },
        )
    except Exception:
        logger.exception('Failed to send websocket notification')
