import prophy
import pytest

def test_optional_scalar():
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = O()
    assert None == x.a
    assert "\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")
    assert """\
""" == str(x)

    x.a = 10
    assert 10 == x.a
    assert "\x00\x00\x00\x01\x00\x00\x00\x0a" == x.encode(">")
    assert "\x01\x00\x00\x00\x0a\x00\x00\x00" == x.encode("<")
    assert """\
a: 10
""" == str(x)

    x.a = None
    assert None == x.a
    assert """\
""" == str(x)

    """ add decoding tests """

def test_optional_struct():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32)]
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(S))]

    x = O()
    assert None == x.a
    assert "\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")
    assert """\
""" == str(x)

    x.a = True
    assert 0 == x.a.a
    assert "\x00\x00\x00\x01\x00\x00\x00\x00" == x.encode(">")
    assert """\
a {
  a: 0
}
""" == str(x)

    x.a.a = 0xFF
    assert 0xFF == x.a.a
    assert "\x00\x00\x00\x01\x00\x00\x00\xFF" == x.encode(">")
    assert "\x01\x00\x00\x00\xFF\x00\x00\x00" == x.encode("<")
    assert """\
a {
  a: 255
}
""" == str(x)

    x.a = None
    assert None == x.a
    assert """\
""" == str(x)

    """ add decoding tests """

def test_optional_union():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 5)]
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(U))]

    x = O()
    assert "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.a = True
    assert "\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x00" == x.encode(">")

    x.a.a = 3
    assert "\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x03" == x.encode(">")

    x.a = None
    assert "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    """ add decoding tests """

def test_optional_bytes():
    """ exception """

def test_optional_array():
    """ exception """

def test_optional_inside_union():
    """ exception """
