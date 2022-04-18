class ParticipantsConsumerMixin:

    def participants_update(self, event):
        data = {
            'type': 'participants.update',
            'participant': event['participant']
        }
        self.send_json(data)

    def participants_delete(self, event):
        data = {
            'type': 'participants.delete',
            'username': event['username']
        }
        self.send_json(data)
