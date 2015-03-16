from . import scalar
from .exception import ProphyError
from .base_array import base_array

def optional(cls):
    if issubclass(cls, bytes):
        raise ProphyError("optional bytes not implemented")
    if issubclass(cls, base_array):
        raise ProphyError("optional array not implemented")
    if cls._DYNAMIC:
        raise ProphyError("optional dynamic fields not implemented")

    class _optional(cls):
        pass

    _optional._OPTIONAL_ALIGNMENT = max(scalar.u32._ALIGNMENT, cls._ALIGNMENT)
    _optional._OPTIONAL_SIZE = _optional._OPTIONAL_ALIGNMENT + cls._SIZE
    _optional._OPTIONAL = True
    _optional._optional_type = scalar.u32
    return _optional
