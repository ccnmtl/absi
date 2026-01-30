import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TranscribeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()
        print('WebSocket connected')

        # Optionally send a welcome message
        await self.send(text_data=json.dumps({
            'message': 'Connected to /ws/'
        }))

    async def disconnect(self, close_code):
        print('WebSocket disconnected', close_code)

    async def receive(self, text_data=None, bytes_data=None):
        # Echo back the message (for testing)
        if text_data:
            data = json.loads(text_data)
            response = {
                'message': f'You said: {data.get('message')}'
            }
            await self.send(text_data=json.dumps(response))
