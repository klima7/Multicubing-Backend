import json
from channels.generic.websocket import JsonWebsocketConsumer
from account.models import Account
from asgiref.sync import async_to_sync
from channels.auth import login, logout
from django.db.models.signals import pre_save


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        authenticated = isinstance(self.scope["user"], Account)

        if not authenticated:
            self.close()
            print('Closed')

        self.accept()
        print('Connected', self.scope["user"])

        async_to_sync(self.channel_layer.group_add)("rooms", self.channel_name)

        # print('Channel', self.channel_name)
        # self.send_json({'type': 'test'})

    def disconnect(self, close_code):
        # await logout(self.scope)
        print('Disconnect', self.scope["user"])
        async_to_sync(self.channel_layer.group_discard)("rooms", self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data_json):
        message = text_data_json['message']

        # Send message to room group
        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def rooms_created(self, event):
        print('rooms_added', event)
        data = {
            'type': 'rooms.added',
            'room': event["room"]
        }
        self.send_json(data)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
