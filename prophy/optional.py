import scalar

def optional(type):
    if "string" in type._tags:
        raise Exception("optional bytes not implemented")
    if "repeated" in type._tags:
        raise Exception("optional array not implemented")
    class _optional(type):
        pass
    _optional._OPTIONAL = True
    _optional._optional_type = scalar.u32
    return _optional
