import scalar

def optional(type):
    class _optional(type):
        pass
    _optional._OPTIONAL = True
    _optional._optional_type = scalar.u32
    _optional._SIZE = type._SIZE + _optional._optional_type._SIZE
    return _optional
