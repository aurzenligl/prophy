import prophy
import pytest

def test_optional_assignment_scalar():
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = O()
    assert None == x.a

    x.a = 10
    assert 10 == x.a

    x.a = None
    assert None == x.a

def test_optional_assignment_struct():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32)]
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(S))]

    x = O()
    assert """\
""" == str(x)

    x.a
    assert """\
a {
  a: 0
}
""" == str(x)

    x.a = None
    assert """\
""" == str(x)
