from channels.generic.websocket import JsonWebsocketConsumer
from channels_presence.decorators import touch_presence
from channels_presence.models import Room

from account.models import Account


class UsersConsumerMixin:

    def users_update(self, event):
        data = {
            'type': 'users.update',
            'user': event['user']
        }
        self.send_json(data)

    def users_delete(self, event):
        data = {
            'type': 'users.delete',
            'username': event['username']
        }
        self.send_json(data)

    def users_refresh(self, event):
        data = {
            'type': 'users.refresh',
        }
        self.send_json(data)


class MessagesConsumerMixin:

    def messages_update(self, event):
        data = {
            'type': 'messages.update',
            'user': event['message']
        }
        self.send_json(data)

    def messages_delete(self, event):
        data = {
            'type': 'messages.delete',
            'id': event['id']
        }
        self.send_json(data)


class RoomConsumer(JsonWebsocketConsumer, UsersConsumerMixin, MessagesConsumerMixin):

    def connect(self):
        user = self.scope['user']
        room_slug = self.scope['url_route']['kwargs']['room_slug']
        authenticated = isinstance(user, Account)

        if not authenticated:
            self.close()

        self.accept()
        Room.objects.add(f'rooms.{room_slug}', self.channel_name, user)

    def disconnect(self, close_code):
        room_slug = self.scope['url_route']['kwargs']['room_slug']
        Room.objects.remove(f'rooms.{room_slug}', self.channel_name)

    @touch_presence
    def receive_json(self, content):
        pass


class RoomsConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope['user']
        authenticated = isinstance(user, Account)

        if not authenticated:
            self.close()

        self.accept()

        Room.objects.add('rooms', self.channel_name, user)

    def disconnect(self, close_code):
        Room.objects.remove('rooms', self.channel_name)

    @touch_presence
    def receive_json(self, content):
        pass

    def rooms_created(self, event):
        data = {
            'type': 'rooms.added',
            'room': event['room']
        }
        self.send_json(data)

    def rooms_deleted(self, event):
        data = {
            'type': 'rooms.deleted',
            'slug': event['slug']
        }
        self.send_json(data)

    def rooms_refresh(self, event):
        data = {
            'type': 'rooms.refresh',
        }
        self.send_json(data)
