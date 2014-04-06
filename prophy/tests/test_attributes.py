import prophy
import pytest

def test_int_attributes():
    assert 1 == prophy.i8._SIZE
    assert False == prophy.i8._DYNAMIC
    assert False == prophy.i8._UNLIMITED
    assert 0 == prophy.i8._DEFAULT

    assert 2 == prophy.i16._SIZE
    assert False == prophy.i16._DYNAMIC
    assert False == prophy.i16._UNLIMITED
    assert 0 == prophy.i16._DEFAULT

    assert 4 == prophy.i32._SIZE
    assert False == prophy.i32._DYNAMIC
    assert False == prophy.i32._UNLIMITED
    assert 0 == prophy.i32._DEFAULT

    assert 8 == prophy.i64._SIZE
    assert False == prophy.i64._DYNAMIC
    assert False == prophy.i64._UNLIMITED
    assert 0 == prophy.i64._DEFAULT

    assert 1 == prophy.u8._SIZE
    assert False == prophy.u8._DYNAMIC
    assert False == prophy.u8._UNLIMITED
    assert 0 == prophy.u8._DEFAULT

    assert 2 == prophy.u16._SIZE
    assert False == prophy.u16._DYNAMIC
    assert False == prophy.u16._UNLIMITED
    assert 0 == prophy.u16._DEFAULT

    assert 4 == prophy.u32._SIZE
    assert False == prophy.u32._DYNAMIC
    assert False == prophy.u32._UNLIMITED
    assert 0 == prophy.u32._DEFAULT

    assert 8 == prophy.u64._SIZE
    assert False == prophy.u64._DYNAMIC
    assert False == prophy.u64._UNLIMITED
    assert 0 == prophy.u64._DEFAULT

def test_float_attributes():
    assert 4 == prophy.r32._SIZE
    assert False == prophy.r32._DYNAMIC
    assert False == prophy.r32._UNLIMITED
    assert 0.0 == prophy.r32._DEFAULT

    assert 8 == prophy.r64._SIZE
    assert False == prophy.r64._DYNAMIC
    assert False == prophy.r64._UNLIMITED
    assert 0.0 == prophy.r64._DEFAULT

def test_enum_attributes():
    class E(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1)]

    assert 4 == E._SIZE
    assert False == E._DYNAMIC
    assert False == E._UNLIMITED
    assert 1 == E._DEFAULT

    class E8(prophy.enum8):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1)]

    assert 1 == E8._SIZE
    assert False == E8._DYNAMIC
    assert False == E8._UNLIMITED
    assert 1 == E8._DEFAULT

def test_bytes_static_attributes():
    B = prophy.bytes(size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '\x00\x00\x00' == B._DEFAULT

def test_bytes_limited_attributes():
    B = prophy.bytes(bound = "a_len", size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT

def test_bytes_bound_attributes():
    B = prophy.bytes(bound = "a_len")

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT

def test_bytes_greedy_attributes():
    B = prophy.bytes()

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert True == B._UNLIMITED
    assert '' == B._DEFAULT

def test_array_static_attributes():
    A = prophy.array(prophy.u16, size = 3)

    assert 6 == A._SIZE
    assert False == A._DYNAMIC
    assert False == A._UNLIMITED

def test_array_limited_attributes():
    A = prophy.array(prophy.u16, bound = "a_len", size = 3)

    assert 6 == A._SIZE
    assert False == A._DYNAMIC
    assert False == A._UNLIMITED

def test_array_bound_attributes():
    A = prophy.array(prophy.u16, bound = "a_len")

    assert 0 == A._SIZE
    assert True == A._DYNAMIC
    assert False == A._UNLIMITED

def test_array_greedy_attributes():
    A = prophy.array(prophy.u16)

    assert 0 == A._SIZE
    assert True == A._DYNAMIC
    assert True == A._UNLIMITED

def test_struct_static_attributes():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("c_len", prophy.u8),
                       ("e_len", prophy.u8),
                       ("b", prophy.bytes(size = 3)),
                       ("c", prophy.bytes(bound = "c_len", size = 3)),
                       ("d", prophy.array(prophy.u8, size = 3)),
                       ("e", prophy.array(prophy.u8, bound = "e_len", size = 3))]
    assert 15 == S._SIZE
    assert False == S._DYNAMIC
    assert False == S._UNLIMITED

    class S1(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", S),
                       ("b_len", prophy.u8),
                       ("b", prophy.array(S, bound = "b_len", size = 3))]

    assert 61 == S1._SIZE
    assert False == S1._DYNAMIC
    assert False == S1._UNLIMITED

def test_struct_dynamic_attributes():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len"))]

    assert 1 == S1._SIZE
    assert True == S1._DYNAMIC
    assert False == S1._UNLIMITED

    class S2(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(S, bound = "a_len"))]

    assert 1 == S2._SIZE
    assert True == S2._DYNAMIC
    assert False == S2._UNLIMITED

    class S3(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", S1),
                       ("b", S2)]

    assert 2 == S3._SIZE
    assert True == S3._DYNAMIC
    assert False == S3._UNLIMITED

def test_struct_unlimited_attributes():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.bytes())]

    assert 0 == S1._SIZE
    assert True == S1._DYNAMIC
    assert True == S1._UNLIMITED

    class S2(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.array(prophy.u8))]

    assert 0 == S2._SIZE
    assert True == S2._DYNAMIC
    assert True == S2._UNLIMITED

    class S3(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", S2)]

    assert 0 == S3._SIZE
    assert True == S3._DYNAMIC
    assert True == S3._UNLIMITED
