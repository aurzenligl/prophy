import prophy
import pytest

def test_optional_assignment_scalar():
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = O()
    assert None == x.a
    assert """\
""" == str(x)

    x.a = 10
    assert 10 == x.a
    assert """\
a: 10
""" == str(x)

    x.a = None
    assert None == x.a
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
    assert None == x.a
    assert """\
""" == str(x)

    x.a = True
    assert 0 == x.a.a
    assert """\
a {
  a: 0
}
""" == str(x)

    x.a = None
    assert None == x.a
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

    """ add decoding tests """

def test_optional_encoding_scalar():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32)]
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(S))]

    x = O()
    assert "\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.a = True
    assert "\x00\x00\x00\x01\x00\x00\x00\x00" == x.encode(">")

    x.a.a = 0xFF
    assert "\x00\x00\x00\x01\x00\x00\x00\xFF" == x.encode(">")
    assert "\x01\x00\x00\x00\xFF\x00\x00\x00" == x.encode("<")

    """ add decoding tests """

def test_optional_encoding_with_enum():
    class E(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", E)]
    class O(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(E)),
                       ("b", prophy.optional(S))]

    x = O()
    assert "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.a = True
    assert "\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.b = True
    assert "\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01" == x.encode(">")

    x.b.a = 3
    assert "\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x03" == x.encode(">")

    x.b = None
    assert "\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    """ add decoding tests """

def test_optional_with_union():
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

""" prohibit:
optional of bytes
optional of array
union with optional
"""
