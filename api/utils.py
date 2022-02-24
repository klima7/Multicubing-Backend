from rest_framework.response import Response


class ErrorResponse(Response):

    def __init__(self, error, message=None, details=None, status=None):
        super().__init__(status=status)
        data = {
            'error': error,
        }
        if message:
            data['message'] = message
        if details:
            data['details'] = details
        self.data = data
