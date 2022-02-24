import json
from channels.generic.websocket import AsyncWebsocketConsumer
from account.models import Account
from channels.auth import login, logout


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        authenticated = isinstance(self.scope["user"], Account)
        if authenticated:
            await self.accept()
            print('Connected', self.scope["user"])
        else:
            await self.close()
            print('Closed')

    async def disconnect(self, close_code):
        # await logout(self.scope)
        print('Disconnect', self.scope["user"])

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
