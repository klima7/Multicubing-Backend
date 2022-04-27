class TurnsConsumerMixin:

    def turns_update(self, event):
        data = {
            'type': 'turns.update',
            'turn': event['turn']
        }
        self.send_json(data)
