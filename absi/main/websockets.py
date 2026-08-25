from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging

from absi.main.utils import get_group_name, GROUP_NAME_PREFIX

logger = logging.getLogger(__name__)


def notify_ws(message: str, azure: bool = False, job_id: str = None):
    """
    Send a JSON-serializable payload to all connected /ws/ clients.
    """
    channel_layer = get_channel_layer()

    if channel_layer is None:
        logger.warning(
            'No channel layer configured; skipping websocket notify')
        return

    group_name = GROUP_NAME_PREFIX
    if job_id:
        group_name = get_group_name(job_id)

    try:
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'send_message',
                'message': message,
                'azure': azure,
            },
        )
    except Exception:
        logger.exception('Failed to send websocket notification')
