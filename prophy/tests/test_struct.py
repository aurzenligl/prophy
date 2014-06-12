import prophy
import pytest

def test_struct_with_dynamic_fields():
    class X(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x_len", prophy.u32),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y", prophy.u32), ]

    assert X._SIZE == 8

    x = X()
    x.x[:] = [1, 2, 3]
    x.y = 4
    assert '\x03\x00\x00\x00\x01\x02\x03\x00\x04\x00\x00\x00' == x.encode('<')

    x.decode('\x01\x00\x00\x00\x01\x00\x00\x00\x08\x00\x00\x00', '<')
    assert x.x[:] == [1]
    assert x.y == 8

def test_struct_exception_with_access_to_nonexistent_field():
    with pytest.raises(AttributeError):
        class X(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", prophy.u32)]
        X().im_not_there

def test_struct_encoding_with_scalars():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u16),
                       ("c", prophy.u8)]
    x = S()

    x.a = 1
    x.b = 2
    x.c = 3
    assert "\x01\x00\x00\x02\x03\x00" == x.encode(">")
    assert "\x01\x00\x02\x00\x03\x00" == x.encode("<")

    assert 6 == x.decode("\x06\x00\x00\x07\x08\x00", ">")
    assert 6 == x.a
    assert 7 == x.b
    assert 8 == x.c

def test_struct_encoding_with_inner_struct():

    class A(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u16),
                       ("b", prophy.u8)]

    class B(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", A),
                       ("b", prophy.u64)]

    x = B()

    x.a.a = 1
    x.a.b = 2
    x.b = 3
    assert "\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03" == x.encode(">")

    assert 16 == x.decode("\x00\x0a\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c", ">")
    assert 0xa == x.a.a
    assert 0xb == x.a.b
    assert 0xc == x.b

def test_struct_encoding_with_arrays():
    class A(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.array(prophy.u8, size = 3)),
                       ("b_len", prophy.u16),
                       ("b", prophy.array(prophy.u32, bound = "b_len"))]

    x = A()

    x.a[:] = [1, 2, 3]
    x.b[:] = [4, 5, 6]
    assert ("\x01\x02\x03\x00"
            "\x00\x03\x00\x00"
            "\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x06") == x.encode(">")

    assert 16 == x.decode(("\x04\x05\x06\x00"
                           "\x00\x02\x00\x00"
                           "\x00\x00\x00\x01\x00\x00\x00\x02"), ">")
    assert [4, 5, 6] == x.a[:]
    assert [1, 2] == x.b[:]

def test_struct_with_multiple_dynamic_fields():
    class A(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u16),
                       ("b_len", prophy.u8),
                       ("a", prophy.array(prophy.u32, bound = "a_len")),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]
    x = A()
    x.a[:] = [1, 2]
    x.b[:] = [3, 4]

    assert '\x00\x02\x02\x00\x00\x00\x00\x01\x00\x00\x00\x02\x03\x04' == x.encode('>')
    assert '\x02\x00\x02\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x04' == x.encode('<')

    x.decode('\x01\x00\x03\x00\x05\x00\x00\x00\x02\x01\x00', '<')
    assert [5] == x.a[:]
    assert [2, 1, 0] == x.b[:]

def test_struct_with_greedy_bytes():
    class A(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u16),
                       ("a", prophy.array(prophy.u16, bound = "a_len")),
                       ("b", prophy.bytes())]
    x = A()
    x.a[:] = [5, 6, 7]
    x.b = 'ala ma kota'

    assert '\x00\x03\x00\x05\x00\x06\x00\x07ala ma kota' == x.encode('>')
    assert '\x03\x00\x05\x00\x06\x00\x07\x00ala ma kota' == x.encode('<')

    x.decode('\x00\x01\x00\x08abecadlo', '>')
    assert [8] == x.a[:]
    assert 'abecadlo' == x.b

def test_struct_with_and_without_padding():
    class A(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u16),
                       ("c", prophy.u64),
                       ("d", prophy.u8)]
    class B(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u16),
                       ("c", prophy.u64),
                       ("d", prophy.u8)]

    x = A()
    x.a = 1
    x.b = 2
    x.c = 3
    x.d = 4

    assert '\x01\x00''\x02\x00\x00\x00\x00\x00''\x03\x00\x00\x00\x00\x00\x00\x00''\x04\x00\x00\x00\x00\x00\x00\x00' == x.encode('<')
    x.decode('\x04\x00''\x05\x00\x00\x00\x00\x00''\x06\x00\x00\x00\x00\x00\x00\x00''\x07\x00\x00\x00\x00\x00\x00\x00', '<')
    assert x.a == 4
    assert x.b == 5
    assert x.c == 6
    assert x.d == 7

    x = B()
    x.a = 1
    x.b = 2
    x.c = 3
    x.d = 4

    assert '\x01''\x02\x00''\x03\x00\x00\x00\x00\x00\x00\x00''\x04' == x.encode('<')
    x.decode('\x04''\x05\x00''\x06\x00\x00\x00\x00\x00\x00\x00''\x07', '<')
    assert x.a == 4
    assert x.b == 5
    assert x.c == 6
    assert x.d == 7

def test_struct_with_substruct_with_bytes():
    class A(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("num_of_x", prophy.u32),
                       ("x", prophy.array(prophy.u8, bound = "num_of_x"))]
    class B(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("num_of_x", prophy.u32),
                       ("x", prophy.array(A, bound = "num_of_x"))]

    x = B()
    x.x.add().x[:] = [1]
    x.x.add().x[:] = [1, 2, 3]
    x.x.add().x[:] = [1, 2, 3, 4, 5, 6, 7]

    assert ('\x03\x00\x00\x00'
            '\x01\x00\x00\x00\x01\x00\x00\x00'
            '\x03\x00\x00\x00\x01\x02\x03\x00'
            '\x07\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x00') == x.encode('<')

    x.decode(('\x02\x00\x00\x00'
              '\x01\x00\x00\x00\x06\x00\x00\x00'
              '\x07\x00\x00\x00\x07\x08\x09\x0a\x0b\x0c\x0d\x00'), '<')
    assert x.x[0].x[:] == [6]
    assert x.x[1].x[:] == [7, 8, 9, 10, 11, 12, 13]

    class C(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", A)]

    x = C()
    x.x.x[:] = [1]
    assert '\x01\x00\x00\x00\x01\x00\x00\x00' == x.encode('<')
