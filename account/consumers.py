from channels.generic.websocket import JsonWebsocketConsumer
from account.models import Account
from channels_presence.models import Room
from channels_presence.decorators import touch_presence


class AccountConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope["user"]
        authenticated = isinstance(user, Account)

        if not authenticated:
            self.close()

        self.accept()
        print(f'User {user} connected')

        Room.objects.add(f'account.{user.username}', self.channel_name, user)

    def disconnect(self, close_code):
        user = self.scope["user"]
        print(f'User {user} disconnected')
        Room.objects.remove(f'account.{user.username}', self.channel_name)

    @touch_presence
    def receive(self, message):
        print(message)
