

class TransactionError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class RangeError(TransactionError):
    pass
