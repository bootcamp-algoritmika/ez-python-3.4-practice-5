class MessageNotFoundException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(MessageNotFoundException, self).__init__(*args, **kwargs)
