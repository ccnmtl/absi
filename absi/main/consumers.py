from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TranscribeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()
        print('WebSocket connected')

        self.group_name = 'transcribe_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Optionally send a welcome message
        await self.send_json({
            'message': 'Record your voice to transcribe it.'
        })

    async def disconnect(self, close_code):
        print('WebSocket disconnected', close_code)
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)

    async def send_transcript(self, event):
        print('send_transcript', event)
        text = event['text']
        await self.send_json({'message': text})
