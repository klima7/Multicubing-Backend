from channels.generic.websocket import JsonWebsocketConsumer
from presence.decorators import touch_presence
from presence.models import Room

from account.models import Account
from message.consumers import MessagesConsumerMixin
from participant.consumers import ParticipantsConsumerMixin
from times.consumers import TurnsConsumerMixin


class RoomConsumer(JsonWebsocketConsumer, MessagesConsumerMixin, ParticipantsConsumerMixin, TurnsConsumerMixin):

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
