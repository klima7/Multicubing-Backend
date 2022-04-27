class TurnsConsumerMixin:

    def turns_update(self, event):
        data = {
            'type': 'turns.update',
            'turn': event['turn']
        }
        self.send_json(data)


class TimesConsumerMixin:

    def times_update(self, event):
        data = {
            'type': 'times.update',
            'time': event['time']
        }
        self.send_json(data)
