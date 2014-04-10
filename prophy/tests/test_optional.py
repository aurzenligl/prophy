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

    x.decode("\x00\x00\x00\x01\x00\x00\x00\x0a", ">")
    assert 10 == x.a

    x.decode("\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert None == x.a

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

    x.decode("\x00\x00\x00\x01\x00\x00\x00\x0a", ">")
    assert 10 == x.a.a

    x.decode("\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert None == x.a

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

    x.decode("\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x03", ">")
    assert 5 == x.a.discriminator
    assert 3 == x.a.a

    x.decode("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert None == x.a

def test_optional_bytes():
    with pytest.raises(Exception) as e:
        prophy.optional(prophy.bytes(size = 3))
    assert "optional bytes not implemented" == e.value.message

def test_optional_array():
    with pytest.raises(Exception) as e:
        prophy.optional(prophy.array(prophy.u8, size = 3))
    assert "optional array not implemented" == e.value.message

def test_optional_inside_union():
    with pytest.raises(Exception) as e:
        class U(prophy.union):
            __metaclass__ = prophy.union_generator
            _descriptor = [("a", prophy.u32, 0),
                           ("b", prophy.optional(prophy.u32), 1),
                           ("c", prophy.u32, 2)]
    assert "union with optional field disallowed" == e.value.message
