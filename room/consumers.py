from channels.generic.websocket import JsonWebsocketConsumer
from account.models import Account
from channels_presence.models import Room
from channels_presence.decorators import touch_presence


class RoomConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope["user"]
        print(self.scope)
        room_slug = self.scope['url_route']['kwargs']['room_slug']
        authenticated = isinstance(user, Account)

        if not authenticated:
            self.close()
            print('Room closed')

        self.accept()
        print('User', user, 'connected to', room_slug)

        Room.objects.add(f'rooms.{room_slug}', self.channel_name, user)
        # async_to_sync(self.channel_layer.group_add)("rooms", self.channel_name)

    def disconnect(self, close_code):
        room_slug = self.scope['url_route']['kwargs']['room_slug']
        print('User', self.scope["user"], 'disconnected from', room_slug)
        Room.objects.remove(f'rooms.{room_slug}', self.channel_name)


class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope["user"]
        authenticated = isinstance(user, Account)

        if not authenticated:
            self.close()
            print('Closed')

        self.accept()
        print('Connected', user)

        Room.objects.add("rooms", self.channel_name, user)
        # async_to_sync(self.channel_layer.group_add)("rooms", self.channel_name)

    def disconnect(self, close_code):
        print('Disconnect', self.scope["user"])
        Room.objects.remove("rooms", self.channel_name)
        # async_to_sync(self.channel_layer.group_discard)("rooms", self.channel_name)

    # Receive message from WebSocket
    @touch_presence
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

    def rooms_deleted(self, event):
        print('rooms_deleted', event)
        data = {
            'type': 'rooms.deleted',
            'slug': event["slug"]
        }
        self.send_json(data)
