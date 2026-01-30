from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify_ws(text: str):
    """
    Send a JSON-serializable payload to all connected /ws/ clients.
    """
    channel_layer = get_channel_layer()
    print('Sending message to group:', text)
    async_to_sync(channel_layer.group_send)(
        'transcribe_updates', {
            'type': 'send_transcript',
            'text': text,
        },
    )
    print('Message sent!')
