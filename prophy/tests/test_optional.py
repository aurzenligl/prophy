import prophy
import pytest

def test_optional_assignment_scalar():
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = O()
    assert """\
""" == str(x)

    x.a
    assert 0 == x.a
    assert """\
a: 0
""" == str(x)

    x.a = 10
    assert 10 == x.a
    assert """\
a: 10
""" == str(x)

    x.a = None
    assert """\
""" == str(x)

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

def test_optional_encoding_scalar():
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = O()
    assert "\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.a = 10
    assert "\x00\x00\x00\x01\x00\x00\x00\x0a" == x.encode(">")
    assert "\x01\x00\x00\x00\x0a\x00\x00\x00" == x.encode("<")
