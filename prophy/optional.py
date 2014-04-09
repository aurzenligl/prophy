def optional(type):
    class _optional(type):
        pass
    _optional._OPTIONAL = True
    return _optional
