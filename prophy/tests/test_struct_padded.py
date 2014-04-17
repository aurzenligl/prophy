import prophy
import pytest

def test_exception_with_dynamic_fields():
    with pytest.raises(Exception) as e:
        class X(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x_len", prophy.u32),
                           ("x", prophy.array(prophy.u8, bound = "x_len")),
                           ("y", prophy.u32), ]
    assert "only last field can be dynamic in padded struct" == e.value.message

def test_exception_with_access_to_nonexistent_field():
    with pytest.raises(AttributeError) as e:
        class X(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", prophy.u32)]
        X().im_not_there

def test_encoding_with_scalars():
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

def test_encoding_with_inner_struct():

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

def test_encoding_with_arrays():
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
