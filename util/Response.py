class Response(dict):
    """
        This class will contain data that will be serialized and returned to caller.
    """
    def __init__(self, status, message, data=None):
        # request status
        self.status = status

        # message for request's response
        self.message = message

        # response data
        self.data = data
