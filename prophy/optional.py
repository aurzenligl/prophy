import scalar
import container

def optional(cls):
    if issubclass(cls, str):
        raise Exception("optional bytes not implemented")
    if issubclass(cls, container.base_array):
        raise Exception("optional array not implemented")

    class _optional(cls):
        pass

    _optional._OPTIONAL = True
    _optional._optional_type = scalar.u32
    return _optional
