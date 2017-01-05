import prophy
import pytest

@pytest.fixture(scope = 'session')
def Struct():
    class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.u32),
                       ("y", prophy.u32)]
    return Struct

@pytest.fixture(scope = 'session')
def NestedStruct(Struct):
    class NestedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", Struct),
                       ("b", Struct)]
    return NestedStruct

@pytest.fixture(scope = 'session')
def DeeplyNestedStruct(NestedStruct, Struct):
    class DeeplyNestedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("m", NestedStruct),
                       ("n", Struct),
                       ("o", prophy.u32)]
    return DeeplyNestedStruct

def test_struct_assignment(Struct):
    x = Struct()

    assert x.x == 0
    assert x.y == 0
    x.x = 3
    x.y = 5

    with pytest.raises(Exception):
        x.nonexistent
    with pytest.raises(Exception):
        x.nonexistent = 10

    y = Struct()
    y.x = 9
    y.y = 9
    y.copy_from(x)
    assert y.x == 3
    assert y.y == 5

    with pytest.raises(Exception):
        y.copy_from("123")
    with pytest.raises(Exception):
        y.copy_from(123)

def test_struct_print(Struct):
    x = Struct()
    x.x = 1
    x.y = 2
    assert str(x) == ("x: 1\n"
                      "y: 2\n")

def test_struct_encode(Struct):
    x = Struct()
    x.x = 1
    x.y = 2
    assert x.encode(">") == (b"\x00\x00\x00\x01"
                             b"\x00\x00\x00\x02")

def test_struct_decode(Struct):
    x = Struct()
    x.decode((b"\x00\x00\x00\x01"
              b"\x00\x00\x00\x02"), ">")
    assert x.x == 1
    assert x.y == 2

def test_nested_struct_assignment(NestedStruct):
    x = NestedStruct()
    assert x.a.x == 0
    assert x.a.y == 0
    assert x.b.x == 0
    assert x.b.y == 0
    x.a.x = 1
    x.a.y = 2
    x.b.x = 3
    x.b.y = 4
    assert x.a.x == 1
    assert x.a.y == 2
    assert x.b.x == 3
    assert x.b.y == 4

    y = NestedStruct()
    y.a.x = 8
    y.a.y = 7
    y.b.x = 6
    y.b.y = 5
    y.copy_from(x)
    assert y.a.x == 1
    assert y.a.y == 2
    assert y.b.x == 3
    assert y.b.y == 4

def test_nested_struct_print(NestedStruct):
    y = NestedStruct()
    y.a.x = 1
    y.a.y = 2
    y.b.x = 3
    y.b.y = 4
    assert str(y) == ("a {\n"
                      "  x: 1\n"
                      "  y: 2\n"
                      "}\n"
                      "b {\n"
                      "  x: 3\n"
                      "  y: 4\n"
                      "}\n"
                      )

def test_nested_struct_encode(NestedStruct):
    y = NestedStruct()
    y.a.x = 1
    y.a.y = 2
    y.b.x = 3
    y.b.y = 4
    assert y.encode(">") == (b"\x00\x00\x00\x01"
                             b"\x00\x00\x00\x02"
                             b"\x00\x00\x00\x03"
                             b"\x00\x00\x00\x04")

def test_nested_struct_decode(NestedStruct):
    y = NestedStruct()
    y.decode((b"\x00\x00\x00\x01"
              b"\x00\x00\x00\x02"
              b"\x00\x00\x00\x03"
              b"\x00\x00\x00\x04"), ">")
    assert y.a.x == 1
    assert y.a.y == 2
    assert y.b.x == 3
    assert y.b.y == 4

def test_deeply_nested_struct_assignment(DeeplyNestedStruct):
    x = DeeplyNestedStruct()
    assert x.m.a.x == 0
    assert x.m.a.y == 0
    assert x.m.b.x == 0
    assert x.m.b.y == 0
    assert x.n.x == 0
    assert x.n.y == 0
    assert x.o == 0
    x.m.a.x = 1
    x.m.a.y = 2
    x.m.b.x = 3
    x.m.b.y = 4
    x.n.x = 5
    x.n.y = 6
    x.o = 7
    assert x.m.a.x == 1
    assert x.m.a.y == 2
    assert x.m.b.x == 3
    assert x.m.b.y == 4
    assert x.n.x == 5
    assert x.n.y == 6
    assert x.o == 7

    with pytest.raises(Exception):
        x.m = 10

    y = DeeplyNestedStruct()
    y.m.a.x = 8
    y.m.a.y = 7
    y.m.b.x = 6
    y.m.b.y = 5
    y.n.x = 4
    y.n.y = 3
    y.o = 2
    y.copy_from(x)
    assert y.m.a.x == 1
    assert y.m.a.y == 2
    assert y.m.b.x == 3
    assert y.m.b.y == 4
    assert y.n.x == 5
    assert y.n.y == 6
    assert y.o == 7

def test_deeply_nested_struct_print(DeeplyNestedStruct):
    z = DeeplyNestedStruct()
    z.m.a.x = 1
    z.m.a.y = 2
    z.m.b.x = 3
    z.m.b.y = 4
    z.n.x = 5
    z.n.y = 6
    z.o = 7
    assert str(z) == ("m {\n"
                      "  a {\n"
                      "    x: 1\n"
                      "    y: 2\n"
                      "  }\n"
                      "  b {\n"
                      "    x: 3\n"
                      "    y: 4\n"
                      "  }\n"
                      "}\n"
                      "n {\n"
                      "  x: 5\n"
                      "  y: 6\n"
                      "}\n"
                      "o: 7\n")

def test_deeply_nested_struct_encode(DeeplyNestedStruct):
    z = DeeplyNestedStruct()
    z.m.a.x = 1
    z.m.a.y = 2
    z.m.b.x = 3
    z.m.b.y = 4
    z.n.x = 5
    z.n.y = 6
    z.o = 7
    assert z.encode(">") == (b"\x00\x00\x00\x01"
                             b"\x00\x00\x00\x02"
                             b"\x00\x00\x00\x03"
                             b"\x00\x00\x00\x04"
                             b"\x00\x00\x00\x05"
                             b"\x00\x00\x00\x06"
                             b"\x00\x00\x00\x07")

def test_deeply_nested_struct_decode(DeeplyNestedStruct):
    z = DeeplyNestedStruct()
    z.decode((b"\x00\x00\x00\x01"
              b"\x00\x00\x00\x02"
              b"\x00\x00\x00\x03"
              b"\x00\x00\x00\x04"
              b"\x00\x00\x00\x05"
              b"\x00\x00\x00\x06"
              b"\x00\x00\x00\x07"), ">")
    assert z.m.a.x == 1
    assert z.m.a.y == 2
    assert z.m.b.x == 3
    assert z.m.b.y == 4
    assert z.n.x == 5
    assert z.n.y == 6
    assert z.o == 7

def test_empty_struct():
    class Empty(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = []

    x = Empty()

    assert "" == str(x)
    assert b"" == x.encode(">")
    assert 0 == x.decode("", ">")

    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", Empty)]

    x = X()

    assert """\
a {
}
""" == str(x)
    assert b"" == x.encode(">")
    assert 0 == x.decode("", ">")

def test_struct_with_dynamic_fields():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u32),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y", prophy.u32)]

    assert X._SIZE == 8

    x = X()
    x.x[:] = [1, 2, 3]
    x.y = 4
    assert b'\x03\x00\x00\x00\x01\x02\x03\x00\x04\x00\x00\x00' == x.encode('<')

    x.decode(b'\x01\x00\x00\x00\x01\x00\x00\x00\x08\x00\x00\x00', '<')
    assert x.x[:] == [1]
    assert x.y == 8

def test_struct_with_many_arrays():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u32),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y_len", prophy.u16),
                       ("y", prophy.array(prophy.u16, bound = "y_len")),
                       ("z_len", prophy.u8),
                       ("z", prophy.array(prophy.u64, bound = "z_len"))]
    x = X()
    x.x[:] = [1, 2, 3, 4, 5]
    x.y[:] = [1, 2]
    x.z[:] = [1, 2, 3]

    assert (b"\x00\x00\x00\x05"
            b"\x01\x02\x03\x04"
            b"\x05\x00"
            b"\x00\x02\x00\x01"
            b"\x00\x02"
            b"\x03\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x01"
            b"\x00\x00\x00\x00\x00\x00\x00\x02"
            b"\x00\x00\x00\x00\x00\x00\x00\x03") == x.encode('>')

def test_struct_with_many_arrays_mixed():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u32),
                       ("y_len", prophy.u16),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y", prophy.array(prophy.u16, bound = "y_len"))]
    x = X()
    x.x[:] = [1, 2, 3, 4, 5]
    x.y[:] = [1, 2]

    assert (b"\x00\x00\x00\x05"
            b"\x00\x02"
            b"\x01\x02\x03\x04"
            b"\x05\x00"
            b"\x00\x01\x00\x02") == x.encode('>')

def test_struct_with_many_arrays_padding():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u8),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y_len", prophy.u32),
                       ("y", prophy.array(prophy.u8, bound = "y_len")),
                       ("z", prophy.u64)]

    class Y(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.u8),
                       ("y", X)]

    x = Y()
    x.x = 1
    x.y.x[:] = [2, 3]
    x.y.y[:] = [4, 5]
    x.y.z = 6

    assert x.encode('>') == (b'\x01\x00\x00\x00'
                             b'\x00\x00\x00\x00'
                             b'\x02\x02\x03\x00'
                             b'\x00\x00\x00\x02'
                             b'\x04\x05\x00\x00'
                             b'\x00\x00\x00\x00'
                             b'\x00\x00\x00\x00'
                             b'\x00\x00\x00\x06')

    x.decode(b'\x05\x00\x00\x00'
             b'\x00\x00\x00\x00'
             b'\x04\x02\x03\x04'
             b'\x05\x00\x00\x00'
             b'\x00\x00\x00\x03'
             b'\x04\x05\x06\x00'
             b'\x00\x00\x00\x00'
             b'\x00\x00\x00\x06', '>')
    assert x.x == 5
    assert x.y.x == [2, 3, 4, 5]
    assert x.y.y == [4, 5, 6]
    assert x.y.z == 6

def test_struct_with_many_arrays_fixed_tail():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u8),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y", prophy.u32),
                       ("z", prophy.u64)]

    x = X()
    x.x[:] = [2, 3]
    x.y = 4
    x.z = 5

    assert x.encode('>') == (b'\x02\x02\x03\x00'
                             b'\x00\x00\x00\x00'
                             b'\x00\x00\x00\x04'
                             b'\x00\x00\x00\x00'
                             b'\x00\x00\x00\x00'
                             b'\x00\x00\x00\x05')

    x.decode((b'\x04\x06\x07\x08'
              b'\x09\x00\x00\x00'
              b'\x00\x00\x00\x05'
              b'\x00\x00\x00\x00'
              b'\x00\x00\x00\x00'
              b'\x00\x00\x00\x06'), '>')
    assert x.x == [6, 7, 8, 9]
    assert x.y == 5
    assert x.z == 6

def test_struct_exception_with_access_to_nonexistent_field():
    with pytest.raises(AttributeError):
        class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
            _descriptor = [("a", prophy.u32)]
        X().im_not_there

def test_struct_encoding_with_scalars():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u16),
                       ("c", prophy.u8)]
    x = S()

    x.a = 1
    x.b = 2
    x.c = 3
    assert b"\x01\x00\x00\x02\x03\x00" == x.encode(">")
    assert b"\x01\x00\x02\x00\x03\x00" == x.encode("<")

    assert 6 == x.decode(b"\x06\x00\x00\x07\x08\x00", ">")
    assert 6 == x.a
    assert 7 == x.b
    assert 8 == x.c

def test_struct_encoding_with_inner_struct():

    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u16),
                       ("b", prophy.u8)]

    class B(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", A),
                       ("b", prophy.u64)]

    x = B()

    x.a.a = 1
    x.a.b = 2
    x.b = 3
    assert b"\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03" == x.encode(">")

    assert 16 == x.decode(b"\x00\x0a\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c", ">")
    assert 0xa == x.a.a
    assert 0xb == x.a.b
    assert 0xc == x.b

def test_struct_encoding_with_arrays():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.array(prophy.u8, size = 3)),
                       ("b_len", prophy.u16),
                       ("b", prophy.array(prophy.u32, bound = "b_len"))]

    x = A()

    x.a[:] = [1, 2, 3]
    x.b[:] = [4, 5, 6]
    assert (b"\x01\x02\x03\x00"
            b"\x00\x03\x00\x00"
            b"\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x06") == x.encode(">")

    assert 16 == x.decode((b"\x04\x05\x06\x00"
                           b"\x00\x02\x00\x00"
                           b"\x00\x00\x00\x01\x00\x00\x00\x02"), ">")
    assert [4, 5, 6] == x.a[:]
    assert [1, 2] == x.b[:]

def test_struct_with_multiple_dynamic_fields():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a_len", prophy.u16),
                       ("b_len", prophy.u8),
                       ("a", prophy.array(prophy.u32, bound = "a_len")),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]
    x = A()
    x.a[:] = [1, 2]
    x.b[:] = [3, 4]

    assert b'\x00\x02\x02\x00\x00\x00\x00\x01\x00\x00\x00\x02\x03\x04\x00\x00' == x.encode('>')
    assert b'\x02\x00\x02\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x04\x00\x00' == x.encode('<')

    x.decode(b'\x01\x00\x03\x00\x05\x00\x00\x00\x02\x01\x00', '<')
    assert [5] == x.a[:]
    assert [2, 1, 0] == x.b[:]

def test_struct_with_greedy_bytes():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a_len", prophy.u16),
                       ("a", prophy.array(prophy.u16, bound = "a_len")),
                       ("b", prophy.bytes())]
    x = A()
    x.a[:] = [5, 6, 7]
    x.b = b'ala ma kota'

    assert b'\x00\x03\x00\x05\x00\x06\x00\x07ala ma kota\x00' == x.encode('>')
    assert b'\x03\x00\x05\x00\x06\x00\x07\x00ala ma kota\x00' == x.encode('<')

    x.decode(b'\x00\x01\x00\x08abacus\x00\x00', '>')
    assert [8] == x.a[:]
    assert b'abacus\x00\x00' == x.b

def test_struct_with_and_without_padding():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u16),
                       ("c", prophy.u64),
                       ("d", prophy.u8)]

    class B(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u16),
                       ("c", prophy.u64),
                       ("d", prophy.u8)]

    x = A()
    x.a = 1
    x.b = 2
    x.c = 3
    x.d = 4

    assert x.encode('<') == (b'\x01\x00'
                             b'\x02\x00\x00\x00\x00\x00'
                             b'\x03\x00\x00\x00\x00\x00\x00\x00'
                             b'\x04\x00\x00\x00\x00\x00\x00\x00')
    x.decode(b'\x04\x00'
             b'\x05\x00\x00\x00\x00\x00'
             b'\x06\x00\x00\x00\x00\x00\x00\x00'
             b'\x07\x00\x00\x00\x00\x00\x00\x00', '<')
    assert x.a == 4
    assert x.b == 5
    assert x.c == 6
    assert x.d == 7

    x = B()
    x.a = 1
    x.b = 2
    x.c = 3
    x.d = 4

    assert b'\x01'b'\x02\x00'b'\x03\x00\x00\x00\x00\x00\x00\x00'b'\x04' == x.encode('<')
    x.decode(b'\x04'b'\x05\x00'b'\x06\x00\x00\x00\x00\x00\x00\x00'b'\x07', '<')
    assert x.a == 4
    assert x.b == 5
    assert x.c == 6
    assert x.d == 7

def test_struct_with_substruct_with_bytes():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("num_of_x", prophy.u32),
                       ("x", prophy.array(prophy.u8, bound = "num_of_x"))]

    class B(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("num_of_x", prophy.u32),
                       ("x", prophy.array(A, bound = "num_of_x"))]

    x = B()
    x.x.add().x[:] = [1]
    x.x.add().x[:] = [1, 2, 3]
    x.x.add().x[:] = [1, 2, 3, 4, 5, 6, 7]

    assert (b'\x03\x00\x00\x00'
            b'\x01\x00\x00\x00\x01\x00\x00\x00'
            b'\x03\x00\x00\x00\x01\x02\x03\x00'
            b'\x07\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x00') == x.encode('<')

    x.decode((b'\x02\x00\x00\x00'
              b'\x01\x00\x00\x00\x06\x00\x00\x00'
              b'\x07\x00\x00\x00\x07\x08\x09\x0a\x0b\x0c\x0d\x00'), '<')
    assert x.x[0].x[:] == [6]
    assert x.x[1].x[:] == [7, 8, 9, 10, 11, 12, 13]

    class C(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", A)]

    x = C()
    x.x.x[:] = [1]
    assert b'\x01\x00\x00\x00\x01\x00\x00\x00' == x.encode('<')
