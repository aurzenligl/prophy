import scalar
import container
from exception import ProphyError

def optional(cls):
    if issubclass(cls, str):
        raise ProphyError("optional bytes not implemented")
    if issubclass(cls, container.base_array):
        raise ProphyError("optional array not implemented")
    if cls._DYNAMIC:
        raise ProphyError("optional dynamic fields not implemented")

    class _optional(cls):
        pass

    _optional._OPTIONAL = True
    _optional._optional_type = scalar.u32
    return _optional
