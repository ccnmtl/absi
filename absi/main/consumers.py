from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TranscribeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()
        print('WebSocket connected')

        self.group_name = 'transcribe_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Optionally send a welcome message
        await self.send_json(content={
            'message': 'Connected to /ws/'
        })

    async def disconnect(self, close_code):
        print('WebSocket disconnected', close_code)
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)

    async def receive_json(self, content=None):
        # Echo back the message (for testing)
        if content:
            d = content
            response = {
                'message': f"You said: {d.get('message')}"
            }
            await self.send_json(content=response)

    async def send_transcript(self, transcript_text):
        print('send_transcript', transcript_text)
        await self.send_json(content={
            'message': transcript_text
        })
