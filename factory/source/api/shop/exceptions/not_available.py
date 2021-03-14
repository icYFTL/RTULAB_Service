class NotAvailable(Exception):
    def __init__(self, message=''):
        super(NotAvailable, self).__init__(message)