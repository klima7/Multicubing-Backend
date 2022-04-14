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
