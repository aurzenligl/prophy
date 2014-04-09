def optional(type):
    class _optional(type):
        _OPTIONAL = True
    return _optional
