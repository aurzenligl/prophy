import prophy
import pytest

def test_int_attributes():
    assert 1 == prophy.i8._SIZE
    assert False == prophy.i8._DYNAMIC
    assert False == prophy.i8._UNLIMITED
    assert 0 == prophy.i8._DEFAULT
    assert False == prophy.i8._OPTIONAL
    assert 1 == prophy.i8._ALIGNMENT

    assert 2 == prophy.i16._SIZE
    assert False == prophy.i16._DYNAMIC
    assert False == prophy.i16._UNLIMITED
    assert 0 == prophy.i16._DEFAULT
    assert False == prophy.i16._OPTIONAL
    assert 2 == prophy.i16._ALIGNMENT

    assert 4 == prophy.i32._SIZE
    assert False == prophy.i32._DYNAMIC
    assert False == prophy.i32._UNLIMITED
    assert 0 == prophy.i32._DEFAULT
    assert False == prophy.i32._OPTIONAL
    assert 4 == prophy.i32._ALIGNMENT

    assert 8 == prophy.i64._SIZE
    assert False == prophy.i64._DYNAMIC
    assert False == prophy.i64._UNLIMITED
    assert 0 == prophy.i64._DEFAULT
    assert False == prophy.i64._OPTIONAL
    assert 8 == prophy.i64._ALIGNMENT

    assert 1 == prophy.u8._SIZE
    assert False == prophy.u8._DYNAMIC
    assert False == prophy.u8._UNLIMITED
    assert 0 == prophy.u8._DEFAULT
    assert False == prophy.u8._OPTIONAL
    assert 1 == prophy.u8._ALIGNMENT

    assert 2 == prophy.u16._SIZE
    assert False == prophy.u16._DYNAMIC
    assert False == prophy.u16._UNLIMITED
    assert 0 == prophy.u16._DEFAULT
    assert False == prophy.u16._OPTIONAL
    assert 2 == prophy.u16._ALIGNMENT

    assert 4 == prophy.u32._SIZE
    assert False == prophy.u32._DYNAMIC
    assert False == prophy.u32._UNLIMITED
    assert 0 == prophy.u32._DEFAULT
    assert False == prophy.u32._OPTIONAL
    assert 4 == prophy.u32._ALIGNMENT

    assert 8 == prophy.u64._SIZE
    assert False == prophy.u64._DYNAMIC
    assert False == prophy.u64._UNLIMITED
    assert 0 == prophy.u64._DEFAULT
    assert False == prophy.u64._OPTIONAL
    assert 8 == prophy.u64._ALIGNMENT

def test_float_attributes():
    assert 4 == prophy.r32._SIZE
    assert False == prophy.r32._DYNAMIC
    assert False == prophy.r32._UNLIMITED
    assert 0.0 == prophy.r32._DEFAULT
    assert 4 == prophy.r32._ALIGNMENT

    assert 8 == prophy.r64._SIZE
    assert False == prophy.r64._DYNAMIC
    assert False == prophy.r64._UNLIMITED
    assert 0.0 == prophy.r64._DEFAULT
    assert 8 == prophy.r64._ALIGNMENT

def test_enum_attributes():
    class E(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1)]

    assert 4 == E._SIZE
    assert False == E._DYNAMIC
    assert False == E._UNLIMITED
    assert 1 == E._DEFAULT
    assert False == E._OPTIONAL
    assert 4 == E._ALIGNMENT

    class E8(prophy.enum8):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1)]

    assert 1 == E8._SIZE
    assert False == E8._DYNAMIC
    assert False == E8._UNLIMITED
    assert 1 == E8._DEFAULT
    assert False == E8._OPTIONAL
    assert 1 == E8._ALIGNMENT

def test_optional_attributes():
    assert 1 == prophy.optional(prophy.i8)._SIZE
    assert False == prophy.optional(prophy.i8)._DYNAMIC
    assert False == prophy.optional(prophy.i8)._UNLIMITED
    assert 0 == prophy.optional(prophy.i8)._DEFAULT
    assert True == prophy.optional(prophy.i8)._OPTIONAL
    assert 1 == prophy.optional(prophy.i8)._ALIGNMENT


def test_bytes_static_attributes():
    B = prophy.bytes(size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '\x00\x00\x00' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT

def test_bytes_limited_attributes():
    B = prophy.bytes(bound = "a_len", size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT

def test_bytes_bound_attributes():
    B = prophy.bytes(bound = "a_len")

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT

def test_bytes_greedy_attributes():
    B = prophy.bytes()

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert True == B._UNLIMITED
    assert '' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT

def test_array_static_attributes():
    A = prophy.array(prophy.u16, size = 3)

    assert 6 == A._SIZE
    assert False == A._DYNAMIC
    assert False == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT

def test_array_limited_attributes():
    A = prophy.array(prophy.u16, bound = "a_len", size = 3)

    assert 6 == A._SIZE
    assert False == A._DYNAMIC
    assert False == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT

def test_array_bound_attributes():
    A = prophy.array(prophy.u16, bound = "a_len")

    assert 0 == A._SIZE
    assert True == A._DYNAMIC
    assert False == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT

def test_array_greedy_attributes():
    A = prophy.array(prophy.u16)

    assert 0 == A._SIZE
    assert True == A._DYNAMIC
    assert True == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT

def test_struct_static_attributes():
    class S(prophy.struct_packed):
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
    assert False == S._OPTIONAL
    assert 1 == S._ALIGNMENT

    class S1(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", S),
                       ("b_len", prophy.u8),
                       ("b", prophy.array(S, bound = "b_len", size = 3))]

    assert 61 == S1._SIZE
    assert False == S1._DYNAMIC
    assert False == S1._UNLIMITED
    assert False == S1._OPTIONAL
    assert 1 == S1._ALIGNMENT
    assert [0, 0, 0] == [padding for _, _, padding in S1._descriptor]

def test_struct_with_optional_attributes():
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32)]
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]
    class O(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.optional(prophy.u32)),
                       ("b", prophy.optional(S)),
                       ("c", prophy.optional(U))]

    assert 28 == O._SIZE
    assert False == O._DYNAMIC
    assert False == O._UNLIMITED
    assert False == O._OPTIONAL
    assert 4 == O._ALIGNMENT
    assert [0, 0, 0] == [padding for _, _, padding in O._descriptor]

def test_struct_dynamic_attributes():
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len"))]

    assert 1 == S1._SIZE
    assert True == S1._DYNAMIC
    assert False == S1._UNLIMITED
    assert False == S1._OPTIONAL
    assert 1 == S1._ALIGNMENT

    class S2(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(S, bound = "a_len"))]

    assert 1 == S2._SIZE
    assert True == S2._DYNAMIC
    assert False == S2._UNLIMITED
    assert False == S2._OPTIONAL
    assert 1 == S2._ALIGNMENT

    class S3(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", S1),
                       ("b", S2)]

    assert 2 == S3._SIZE
    assert True == S3._DYNAMIC
    assert False == S3._UNLIMITED
    assert False == S3._OPTIONAL
    assert 1 == S3._ALIGNMENT

def test_struct_unlimited_attributes():
    class S(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.bytes())]

    assert 0 == S1._SIZE
    assert True == S1._DYNAMIC
    assert True == S1._UNLIMITED
    assert False == S1._OPTIONAL
    assert 1 == S._ALIGNMENT

    class S2(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.array(prophy.u8))]

    assert 0 == S2._SIZE
    assert True == S2._DYNAMIC
    assert True == S2._UNLIMITED
    assert False == S2._OPTIONAL
    assert 1 == S2._ALIGNMENT

    class S3(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", S2)]

    assert 0 == S3._SIZE
    assert True == S3._DYNAMIC
    assert True == S3._UNLIMITED
    assert False == S3._OPTIONAL
    assert 1 == S3._ALIGNMENT

def test_struct_padded():
    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u32),
                       ("c", prophy.u64)]

    assert 8 == S._ALIGNMENT
    assert 16 == S._SIZE
    assert [3, 0, 0] == [padding for _, _, padding in S._descriptor]

    class S2(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32),
                       ("b", S)]

    assert 8 == S2._ALIGNMENT
    assert 24 == S2._SIZE
    assert [4, 0] == [padding for _, _, padding in S2._descriptor]

    class S3(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u32),
                       ("b", prophy.u8)]

    assert 4 == S3._ALIGNMENT
    assert 8 == S3._SIZE
    assert [0, 3] == [padding for _, _, padding in S3._descriptor]

    class S4(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.array(prophy.u8, size = 7)),
                       ("b", prophy.u32)]

    assert 4 == S4._ALIGNMENT
    assert 12 == S4._SIZE
    assert [1, 0] == [padding for _, _, padding in S4._descriptor]

    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    class S5(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", prophy.u8),
                       ("b", U),
                       ("c", prophy.u8)]

    assert 4 == S5._ALIGNMENT
    assert 16 == S5._SIZE
    assert [3, 0, 3] == [padding for _, _, padding in S5._descriptor]

def test_union_attributes():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    assert 8 == U._SIZE
    assert False == U._DYNAMIC
    assert False == U._UNLIMITED
    assert False == U._OPTIONAL
    assert 4 == U._ALIGNMENT
