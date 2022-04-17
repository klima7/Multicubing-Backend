from channels.generic.websocket import JsonWebsocketConsumer
from presence.decorators import touch_presence
from presence.models import Room as RoomPresence

from account.models import Account


class AccountConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope["user"]
        authenticated = isinstance(user, Account)

        if not authenticated:
            self.close()

        self.accept()

        RoomPresence.objects.add(f'account.{user.username}', self.channel_name, user)

    def disconnect(self, close_code):
        user = self.scope["user"]
        RoomPresence.objects.remove(f'account.{user.username}', self.channel_name)

    @touch_presence
    def receive_json(self, content):
        pass


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
