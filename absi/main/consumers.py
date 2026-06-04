import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from absi.main.util import GROUP_NAME

logger = logging.getLogger(__name__)


class TranscribeConsumer(AsyncJsonWebsocketConsumer):
    group_name = GROUP_NAME

    async def connect(self):
        # Accept the connection
        await self.accept()
        print('WebSocket connected')

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Optionally send a welcome message
        await self.send_json({
            'message': 'Record your voice for pronunciation assessment.',
            'azure': True,
        })

    async def disconnect(self, close_code):
        print('WebSocket disconnected', close_code)
        try:
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name)
        except Exception:
            logger.exception('Error discarding websocket group')

    async def send_message(self, event):
        print('send_message', event)

        try:
            await self.send_json({
                'message': event.get('message', ''),
                'azure': event.get('azure', False),
            })
        except Exception:
            logger.exception('Error sending websocket message')
