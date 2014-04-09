import prophy
import pytest

def test_optional():
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = O()

