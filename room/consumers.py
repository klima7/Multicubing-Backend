import json
from channels.generic.websocket import WebsocketConsumer
from account.models import Account
from channels.auth import login, logout


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        authenticated = isinstance(self.scope["user"], Account)
        if authenticated:
            self.accept()
            print('Connected', self.scope["user"])
        else:
            self.close()
            print('Closed')

    def disconnect(self, close_code):
        # await logout(self.scope)
        print('Disconnect', self.scope["user"])

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
