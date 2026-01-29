from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify_ws(data: dict):
    """
    Send a JSON-serializable payload to all connected /ws/ clients.
    """
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'transcribe_ws', {
            'type': 'ws_notify',
            'data': data,
        },
    )
