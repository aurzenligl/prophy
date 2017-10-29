import prophy
import pytest

def test_optional_scalar():
    class K(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.optional(prophy.u32))]

    x = K()
    assert x.a is None
    assert x.encode(">") == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert str(x) == """\
"""

    x.a = 10
    assert x.a == 10
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x0a"
    assert x.encode("<") == b"\x01\x00\x00\x00\x0a\x00\x00\x00"
    assert str(x) == """\
a: 10
"""

    x.a = None
    assert x.a is None
    assert str(x) == """\
"""

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x0a", ">")
    assert x.a == 10

    x.decode(b"\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert x.a is None

def test_optional_struct():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u32)]

    class K(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.optional(S))]

    x = K()
    assert x.a is None
    assert x.encode(">") == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    assert str(x) == """\
"""

    x.a = True
    assert x.a.a == 0
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x00"
    assert str(x) == """\
a {
  a: 0
}
"""

    x.a.a = 0xFF
    assert x.a.a == 0xFF
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\xFF"
    assert x.encode("<") == b"\x01\x00\x00\x00\xFF\x00\x00\x00"
    assert str(x) == """\
a {
  a: 255
}
"""

    x.a = None
    assert x.a is None
    assert str(x) == """\
"""

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x0a", ">")
    assert x.a.a == 10

    x.decode(b"\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert x.a is None

def test_optional_union():
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u32, 5)]

    class K(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.optional(U))]

    x = K()
    assert x.encode(">") == b"\x00\x00\x00\x00" b"\x00\x00\x00\x00\x00\x00\x00\x00"

    x.a = True
    assert x.encode(">") == b"\x00\x00\x00\x01" b"\x00\x00\x00\x05" b"\x00\x00\x00\x00"

    x.a.a = 3
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x03"

    x.a = None
    assert x.encode(">") == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x03", ">")
    assert x.a.discriminator == 5
    assert x.a.a == 3

    x.decode(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert x.a is None

def test_optional_struct_in_array():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [('a', prophy.u32),
                       ('b', prophy.u32)]

    class B(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [('a', prophy.optional(A))]

    class C(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [('a_len', prophy.u32),
                       ('a', prophy.array(B, bound = 'a_len'))]

    x = C()
    x.a.add()
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", ">")
    assert str(x) == """\
a {
}
"""

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00\x03", ">")
    assert str(x) == """\
a {
  a {
    a: 6
    b: 3
  }
}
"""

def test_optional_bytes():
    with pytest.raises(Exception) as e:
        prophy.optional(prophy.bytes(size = 3))
    assert "optional bytes not implemented" == str(e.value)

def test_optional_dynamic_field():
    class Dynamic(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('a_len', prophy.u32),
                       ('a', prophy.array(prophy.u8, bound = 'a_len'))]
    with pytest.raises(Exception) as e:
        prophy.optional(Dynamic)
    assert "optional dynamic fields not implemented" == str(e.value)

def test_optional_array():
    with pytest.raises(Exception) as e:
        prophy.optional(prophy.array(prophy.u8, size = 3))
    assert "optional array not implemented" == str(e.value)

    with pytest.raises(Exception) as e:
        class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a_len", prophy.optional(prophy.u32)),
                           ("a", prophy.array(prophy.u32, bound = "a_len"))]
    assert "array S.a must not be bound to optional field" == str(e.value)

    with pytest.raises(Exception) as e:
        prophy.array(prophy.optional(prophy.u32))
    assert "array of optional type not allowed" == str(e.value)

def test_optional_padded():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('x', prophy.optional(prophy.u8)),
                       ('y', prophy.optional(prophy.u64))]

    x = X()
    x.x = 1
    x.y = 2
    assert x.encode('>') == (
        b'\x00\x00\x00\x01'
        b'\x01\x00\x00\x00'
        b'\x00\x00\x00\x01\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x02'
    )
    x.decode(
        b'\x00\x00\x00\x01'
        b'\x03\x00\x00\x00'
        b'\x00\x00\x00\x01\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x04',
        '>'
    )
    assert x.x == 3
    assert x.y == 4
    assert str(x) == """\
x: 3
y: 4
"""
