from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TranscribeConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'transcribe_updates'

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
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)

    async def send_message(self, event):
        print('send_message', event)
        text = event['text']
        azure = event.get('azure', None)
        await self.send_json({
            'message': text,
            'azure': azure,
        })
