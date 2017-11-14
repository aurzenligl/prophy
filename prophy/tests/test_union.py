import prophy
import pytest

@pytest.fixture(scope = 'session')
def SimpleUnion():
    class SimpleUnion(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u32, 1),
                       ("c", prophy.u32, 2)]
    return SimpleUnion

@pytest.fixture(scope = 'session')
def VariableLengthFieldsUnion():
    class VariableLengthFieldsUnion(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2),
                       ("d", prophy.u64, 3)]
    return VariableLengthFieldsUnion

def test_simple_union(SimpleUnion):
    x = SimpleUnion()

    assert 0 == x.discriminator
    assert 0 == x.a
    assert 'a: 0\n' == str(x)
    assert b'\x00\x00\x00\x00\x00\x00\x00\x00' == x.encode(">")

    x.decode(b'\x02\x00\x00\x00\x10\x00\x00\x00', "<")

    assert 2 == x.discriminator
    assert 16 == x.c
    assert 'c: 16\n' == str(x)
    assert b'\x00\x00\x00\x02\x00\x00\x00\x10' == x.encode(">")

def test_simple_union_discriminator_accepts_ints_or_field_name_and_clears(SimpleUnion):
    x = SimpleUnion()

    x.a = 42
    x.discriminator = 1

    assert 0 == x.b
    assert 'b: 0\n' == str(x)
    assert b'\x00\x00\x00\x01\x00\x00\x00\x00' == x.encode(">")

    x.discriminator = "c"

    assert 0 == x.c
    assert 'c: 0\n' == str(x)
    assert b'\x00\x00\x00\x02\x00\x00\x00\x00' == x.encode(">")

def test_union_copy_from(SimpleUnion):
    x = SimpleUnion()
    x.discriminator = 'b'
    x.b = 3

    y = SimpleUnion()
    y.discriminator = 'c'
    y.c = 10
    y.copy_from(x)
    assert 1 == y.discriminator
    assert 3 == y.b

    y.copy_from(y)
    assert y == y
    assert 1 == y.discriminator
    assert 3 == y.b

def test_simple_union_discriminator_does_not_clear_fields_if_set_to_same_value(SimpleUnion):
    x = SimpleUnion()

    x.a = 42

    x.discriminator = 0

    assert 42 == x.a

    x.discriminator = "a"

    assert 42 == x.a

def test_union_nonsequential_discriminators():
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u32, 3),
                       ("b", prophy.u32, 10),
                       ("c", prophy.u32, 55)]
    x = U()
    assert 3 == x.discriminator

    x.discriminator = 3
    assert 3 == x.discriminator
    assert 0 == x.a

    x.discriminator = 10
    assert 10 == x.discriminator
    assert 0 == x.b

    x.discriminator = 55
    assert 55 == x.discriminator
    assert 0 == x.c

    x.discriminator = "a"
    assert 3 == x.discriminator
    assert 0 == x.a

    x.discriminator = "b"
    assert 10 == x.discriminator
    assert 0 == x.b

    x.discriminator = "c"
    assert 55 == x.discriminator
    assert 0 == x.c

def test_union_encode_according_to_largest_field(VariableLengthFieldsUnion):
    x = VariableLengthFieldsUnion()

    x.discriminator = "a"
    x.a = 0x12
    assert b"\x00\x00\x00\x00\x00\x00\x00\x00" b"\x12\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")
    assert b"\x00\x00\x00\x00\x00\x00\x00\x00" b"\x12\x00\x00\x00\x00\x00\x00\x00" == x.encode("<")

    x.discriminator = "b"
    x.b = 0x1234
    assert b"\x00\x00\x00\x01\x00\x00\x00\x00" b"\x12\x34\x00\x00\x00\x00\x00\x00" == x.encode(">")
    assert b"\x01\x00\x00\x00\x00\x00\x00\x00" b"\x34\x12\x00\x00\x00\x00\x00\x00" == x.encode("<")

    x.discriminator = "c"
    x.c = 0x12345678
    assert b"\x00\x00\x00\x02\x00\x00\x00\x00" b"\x12\x34\x56\x78\x00\x00\x00\x00" == x.encode(">")
    assert b"\x02\x00\x00\x00\x00\x00\x00\x00" b"\x78\x56\x34\x12\x00\x00\x00\x00" == x.encode("<")

    x.discriminator = "d"
    x.d = 0x123456789ABCDEF1
    assert b"\x00\x00\x00\x03\x00\x00\x00\x00" b"\x12\x34\x56\x78\x9a\xbc\xde\xf1" == x.encode(">")
    assert b"\x03\x00\x00\x00\x00\x00\x00\x00" b"\xf1\xde\xbc\x9a\x78\x56\x34\x12" == x.encode("<")

def test_union_decode_according_to_largest_field(VariableLengthFieldsUnion):
    x = VariableLengthFieldsUnion()

    assert 16 == x.decode(b"\x00\x00\x00\x00\x00\x00\x00\x00" b"\x12\x00\x00\x00\x00\x00\x00\x00", ">")
    assert 0 == x.discriminator
    assert 0x12 == x.a

    assert 16 == x.decode(b"\x00\x00\x00\x00\x00\x00\x00\x00" b"\x12\x00\x00\x00\x00\x00\x00\x00", "<")
    assert 0 == x.discriminator
    assert 0x12 == x.a

    assert 16 == x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x00" b"\x12\x34\x00\x00\x00\x00\x00\x00", ">")
    assert 1 == x.discriminator
    assert 0x1234 == x.b

    assert 16 == x.decode(b"\x01\x00\x00\x00\x00\x00\x00\x00" b"\x34\x12\x00\x00\x00\x00\x00\x00", "<")
    assert 1 == x.discriminator
    assert 0x1234 == x.b

    assert 16 == x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x00" b"\x12\x34\x56\x78\x00\x00\x00\x00", ">")
    assert 2 == x.discriminator
    assert 0x12345678 == x.c

    assert 16 == x.decode(b"\x02\x00\x00\x00\x00\x00\x00\x00" b"\x78\x56\x34\x12\x00\x00\x00\x00", "<")
    assert 2 == x.discriminator
    assert 0x12345678 == x.c

    assert 16 == x.decode(b"\x00\x00\x00\x03\x00\x00\x00\x00" b"\x12\x34\x56\x78\x9a\xbc\xde\xf1", ">")
    assert 3 == x.discriminator
    assert 0x123456789ABCDEF1 == x.d

    assert 16 == x.decode(b"\x03\x00\x00\x00\x00\x00\x00\x00" b"\xf1\xde\xbc\x9a\x78\x56\x34\x12", "<")
    assert 3 == x.discriminator
    assert 0x123456789ABCDEF1 == x.d

def test_union_with_struct():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u32),
                       ("b", prophy.u32)]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u16, 0),
                       ("b", S, 1)]

    x = U()
    assert x.encode(">") == b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    x.a = 0x15
    assert x.encode(">") == b"\x00\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00"
    assert x.encode("<") == b"\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00"

    x.discriminator = "b"
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00"
    assert x.encode("<") == b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    x.b.a = 0x15
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x15\x00\x00\x00\x00"
    assert x.encode("<") == b"\x01\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00"
    x.b.b = 0x20
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x15\x00\x00\x00\x20"
    assert x.encode("<") == b"\x01\x00\x00\x00\x15\x00\x00\x00\x20\x00\x00\x00"

    x.decode(b"\x00\x00\x00\x00\x25\x00\x00\x00\x00\x00\x00\x00", "<")
    assert x.discriminator == 0
    assert x.a == 0x25

    x.decode(b"\x00\x00\x00\x00\x00\x25\x00\x00\x00\x00\x00\x00", ">")
    assert x.discriminator == 0
    assert x.a == 0x25

    with pytest.raises(prophy.ProphyError) as err:
        x.b
    assert str(err.value) == 'currently field 0 is discriminated'

    x.decode(b"\x01\x00\x00\x00\x25\x00\x00\x00\x35\x00\x00\x00", "<")
    assert x.discriminator == 1
    assert x.b.a == 0x25
    assert x.b.b == 0x35

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x25\x00\x00\x00\x35", ">")
    assert x.discriminator == 1
    assert x.b.a == 0x25
    assert x.b.b == 0x35

    with pytest.raises(prophy.ProphyError) as err:
        x.b = 'anythig'
    assert str(err.value) == 'assignment to composite field not allowed'

def test_union_discriminator_exceptions(VariableLengthFieldsUnion):
    x = VariableLengthFieldsUnion()

    with pytest.raises(Exception) as e:
        x.b
    assert "currently field 0 is discriminated" == str(e.value)

    x.discriminator = 1
    x.b = 42

    with pytest.raises(Exception) as e:
        x.a
    assert "currently field 1 is discriminated" == str(e.value)

    with pytest.raises(Exception) as e:
        x.a = 1
    assert "currently field 1 is discriminated" == str(e.value)

    with pytest.raises(Exception) as e:
        x.discriminator = "xxx"
    assert "unknown discriminator" == str(e.value)

    with pytest.raises(Exception) as e:
        x.discriminator = 666
    assert "unknown discriminator" == str(e.value)

    assert 1 == x.discriminator
    assert 42 == x.b

def test_union_decode_exceptions(VariableLengthFieldsUnion):
    x = VariableLengthFieldsUnion()

    with pytest.raises(Exception) as e:
        x.decode(b"\x00\x00\x00\xff", ">")
    assert "unknown discriminator" == str(e.value)

    with pytest.raises(Exception) as e:
        x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x00" b"\x12\x34\x56\x78\x00\x00\x00\x00\x00", ">")
    assert "not all bytes of VariableLengthFieldsUnion read" == str(e.value)

    with pytest.raises(Exception) as e:
        x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x00" b"\x12\x34\x56\x78\x00\x00\x00", ">")
    assert "not enough bytes" == str(e.value)

def test_struct_with_union():
    class UVarLen(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u8, 1),
                       ("c", prophy.u8, 2)]

    class StructWithU(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8),
                       ("b", UVarLen),
                       ("c", prophy.u32)]

    x = StructWithU()

    x.a = 1
    x.b.discriminator = 2
    x.b.c = 3
    x.c = 4

    assert b"\x01\x00\x00\x00" b"\x00\x00\x00\x02" b"\x03\x00\x00\x00" b"\x00\x00\x00\x04" == x.encode(">")
    assert b"\x01\x00\x00\x00" b"\x02\x00\x00\x00" b"\x03\x00\x00\x00" b"\x04\x00\x00\x00" == x.encode("<")

    x.decode(b"\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x20", ">")

    assert 10 == x.a
    assert 0 == x.b.discriminator
    assert 1024 == x.b.a
    assert 32 == x.c

    assert """\
a: 10
b {
  a: 1024
}
c: 32
""" == str(x)

def test_array_with_union():
    class UVarLen(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u16, 0),
                       ("b", prophy.u8, 1),
                       ("c", prophy.u8, 2)]

    class StructWithU(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(UVarLen, bound = "a_len"))]

    x = StructWithU()

    y = x.a.add()
    y.discriminator = "a"
    y.a = 1
    y = x.a.add()
    y.discriminator = "b"
    y.b = 2
    y = x.a.add()
    y.discriminator = "c"
    y.c = 3

    assert x.encode(">") == (b"\x03\x00\x00\x00"
                             b"\x00\x00\x00\x00"
                             b"\x00\x01\x00\x00"
                             b"\x00\x00\x00\x01"
                             b"\x02\x00\x00\x00"
                             b"\x00\x00\x00\x02"
                             b"\x03\x00\x00\x00")
    assert x.encode("<") == (b"\x03\x00\x00\x00"
                             b"\x00\x00\x00\x00"
                             b"\x01\x00\x00\x00"
                             b"\x01\x00\x00\x00"
                             b"\x02\x00\x00\x00"
                             b"\x02\x00\x00\x00"
                             b"\x03\x00\x00\x00")

    x.decode(b"\x02\x00\x00\x00"
             b"\x00\x00\x00\x01"
             b"\x01\x00\x00\x00"
             b"\x00\x00\x00\x02"
             b"\x02\x00\x00\x00", ">")

    assert """\
a {
  b: 1
}
a {
  c: 2
}
""" == str(x)

def test_union_with_plain_struct():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u8)]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", S, 1)]

    x = U()
    x.discriminator = 1
    x.b.a = 2
    x.b.b = 3

    assert b"\x00\x00\x00\x01\x02\x03\x00\x00" == x.encode(">")

    x.decode(b"\x00\x00\x00\x01\x06\x07\x00\x00", ">")
    assert 1 == x.discriminator
    assert 6 == x.b.a
    assert 7 == x.b.b

    assert """\
b {
  a: 6
  b: 7
}
""" == str(x)

def test_union_with_struct_with_array_and_bytes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8)]

    class SBytesSized(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.bytes(size = 3))]

    class SArraySized(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.array(S, size = 3))]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", SBytesSized, 0),
                       ("b", SArraySized, 1)]

    x = U()
    x.discriminator = 0
    x.a.a = b"abc"

    assert b"\x00\x00\x00\x00" b"abc\x00" == x.encode(">")

    x.discriminator = 1
    x.b.a[0].a = 3
    x.b.a[1].a = 4
    x.b.a[2].a = 5
    assert b"\x00\x00\x00\x01" b"\x03\x04\x05\x00" == x.encode(">")

    x.decode(b"\x00\x00\x00\x01" b"\x07\x08\x09\x00", ">")
    assert 1 == x.discriminator
    assert 7 == x.b.a[0].a
    assert 8 == x.b.a[1].a
    assert 9 == x.b.a[2].a

    assert """\
b {
  a {
    a: 7
  }
  a {
    a: 8
  }
  a {
    a: 9
  }
}
""" == str(x)

def test_union_with_nested_struct_and_union():
    class SInner(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8)]

    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", SInner)]

    class UInner(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1)]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", UInner, 0),
                       ("b", S, 1)]

    x = U()
    x.discriminator = 0
    x.a.discriminator = 1
    x.a.b = 0xFFF
    assert b"\x00\x00\x00\x00" b"\x00\x00\x00\x01" b"\x0f\xff\x00\x00" == x.encode(">")

    x = U()
    x.discriminator = 1
    x.b.a.a = 0xF
    assert b"\x00\x00\x00\x01" b"\x0f\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.decode(b"\x00\x00\x00\x00" b"\x00\x00\x00\x01" b"\x00\x08\x00\x00", ">")
    assert 8 == x.a.b

    assert """\
a {
  b: 8
}
""" == str(x)

    y = U()
    y.copy_from(x)
    assert 0 == y.discriminator
    assert 1 == y.a.discriminator
    assert 8 == y.a.b

def test_union_with_typedef_and_enum():
    TU16 = prophy.u16

    class E(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", TU16, 0),
                       ("b", E, 1)]

    x = U()
    x.discriminator = "a"
    x.a = 17
    assert b"\x00\x00\x00\x00\x00\x11\x00\x00" == x.encode(">")

    x.discriminator = "b"
    x.b = "E_2"
    assert b"\x00\x00\x00\x01\x00\x00\x00\x02" == x.encode(">")

    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x01", ">")
    assert 1 == x.discriminator
    assert 1 == x.b

    assert """\
b: E_1
""" == str(x)

def test_union_exceptions_with_dynamic_arrays_and_bytes():
    with pytest.raises(Exception) as e:
        class U1(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a", prophy.array(prophy.u32), 0)]
    assert "dynamic types not allowed in union" == str(e.value)

    with pytest.raises(Exception) as e:
        class U2(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.array(prophy.u32, bound = "a_len"), 1)]
    assert "dynamic types not allowed in union" == str(e.value)

    with pytest.raises(Exception) as e:
        class U3(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a", prophy.bytes(), 0)]
    assert "dynamic types not allowed in union" == str(e.value)

    with pytest.raises(Exception) as e:
        class U4(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.bytes(bound = "a_len"), 1)]
    assert "dynamic types not allowed in union" == str(e.value)

def test_union_exceptions_with_nested_limited_greedy_dynamic_arrays_and_bytes():
    with pytest.raises(Exception) as e:
        class S2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a", prophy.array(prophy.u32))]

        class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a", S2)]

        class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a", S, 0)]
    assert "dynamic types not allowed in union" == str(e.value)

def test_union_with_limited_array_and_bytes():
    with pytest.raises(Exception) as e:
        class U1(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.bytes(bound = "a_len", size = 3), 1)]
    assert "bound array/bytes not allowed in union" == str(e.value)

    with pytest.raises(Exception) as e:
        class U2(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a_len", prophy.u8, 0),
                           ("a", prophy.array(prophy.u32, bound = "a_len", size = 3), 1)]
    assert "bound array/bytes not allowed in union" == str(e.value)

    with pytest.raises(Exception) as e:
        class U3(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a", prophy.array(prophy.u8, size = 3), 0)]
    assert "static array not implemented in union" == str(e.value)

def test_union_with_static_bytes():
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.bytes(size = 3), 0)]

    x = U()

    assert b"\x00\x00\x00\x00" b"\x00\x00\x00\x00" == x.encode(">")

    x.decode(b"\x00\x00\x00\x00" b"\x01\x02\x03\x00", "<")

    assert """\
a: '\\x01\\x02\\x03'
""" == str(x)

def test_union_with_optional_exception():
    with pytest.raises(Exception) as e:
        class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
            _descriptor = [("a", prophy.u32, 0),
                           ("b", prophy.optional(prophy.u32), 1),
                           ("c", prophy.u32, 2)]
    assert "union with optional field disallowed" == str(e.value)
