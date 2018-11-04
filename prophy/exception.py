CONSTRAINT_VIOLATION, TOO_MANY_BYTES, NOT_ENOUGH_BYTES = range(3)


class ProphyError(Exception):
    pass


class DecodeError(ProphyError):
    def __init__(self, message, subtype=None):
        super(DecodeError, self).__init__(message)
        self.subtype = subtype
