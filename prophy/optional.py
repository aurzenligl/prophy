import scalar

def optional(cls):
    if "string" in cls._tags:
        raise Exception("optional bytes not implemented")
    if "repeated" in cls._tags:
        raise Exception("optional array not implemented")

    class _optional(cls):
        pass

    _optional._OPTIONAL = True
    _optional._optional_type = scalar.u32
    return _optional
