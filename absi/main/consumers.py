import logging
import uuid
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from absi.main.utils import get_group_name

logger = logging.getLogger(__name__)


class TranscribeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Custom group name for each websocket connection
        self.job_id = uuid.uuid4().hex
        self.group_name = get_group_name(self.job_id)

        # Accept the connection
        await self.accept()
        print('WebSocket connected')

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Optionally send a welcome message
        await self.send_json({
            'message': 'Record your voice for pronunciation assessment.',
            'connect': True,
            'job_id': self.job_id,
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
