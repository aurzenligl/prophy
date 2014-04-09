def optional(type):

    class _optional(type):

        @staticmethod
        def _check(value):
            return None if value is None else type._check(value)

    _optional._DEFAULT = None
    _optional._OPTIONAL = True
    return _optional
