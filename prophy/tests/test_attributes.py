import prophy
import pytest

@pytest.mark.parametrize("tp, size", [
    (prophy.i8, 1),
    (prophy.i16, 2),
    (prophy.i32, 4),
    (prophy.i64, 8),
    (prophy.u8, 1),
    (prophy.u16, 2),
    (prophy.u32, 4),
    (prophy.u64, 8)
])
def test_int_attributes(tp, size):
    assert tp._SIZE == size
    assert tp._DYNAMIC == False
    assert tp._UNLIMITED == False
    assert tp._DEFAULT == 0
    assert tp._OPTIONAL == False
    assert tp._ALIGNMENT == size
    assert tp._BOUND is None
    assert tp._PARTIAL_ALIGNMENT is None

@pytest.mark.parametrize("tp, size", [
    (prophy.r32, 4),
    (prophy.r64, 8)
])
def test_float_attributes(tp, size):
    assert tp._SIZE == size
    assert tp._DYNAMIC == False
    assert tp._UNLIMITED == False
    assert tp._DEFAULT == 0.0
    assert tp._OPTIONAL == False
    assert tp._ALIGNMENT == size
    assert tp._BOUND is None
    assert tp._PARTIAL_ALIGNMENT is None

def make_E():
    class E(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("E_1", 1)]
    return E

def make_E8():
    class E8(prophy.with_metaclass(prophy.enum_generator, prophy.enum8)):
        _enumerators = [("E_1", 1)]
    return E8

@pytest.mark.parametrize("tp_factory, size", [
    (make_E, 4),
    (make_E8, 1)
])
def test_enum_attributes(tp_factory, size):
    assert tp_factory()._SIZE == size
    assert tp_factory()._DYNAMIC == False
    assert tp_factory()._UNLIMITED == False
    assert tp_factory()._DEFAULT == 1
    assert tp_factory()._OPTIONAL == False
    assert tp_factory()._ALIGNMENT == size
    assert tp_factory()._BOUND is None
    assert tp_factory()._PARTIAL_ALIGNMENT is None

def test_optional_attributes():
    assert 1 == prophy.optional(prophy.i8)._SIZE
    assert False == prophy.optional(prophy.i8)._DYNAMIC
    assert False == prophy.optional(prophy.i8)._UNLIMITED
    assert 0 == prophy.optional(prophy.i8)._DEFAULT
    assert True == prophy.optional(prophy.i8)._OPTIONAL
    assert 1 == prophy.optional(prophy.i8)._ALIGNMENT
    assert None == prophy.optional(prophy.i8)._BOUND
    assert None == prophy.optional(prophy.i8)._PARTIAL_ALIGNMENT

    assert 5 == prophy.optional(prophy.i8)._OPTIONAL_SIZE
    assert 4 == prophy.optional(prophy.i8)._OPTIONAL_ALIGNMENT
    assert 16 == prophy.optional(prophy.i64)._OPTIONAL_SIZE
    assert 8 == prophy.optional(prophy.i64)._OPTIONAL_ALIGNMENT

def test_bytes_static_attributes():
    B = prophy.bytes(size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert b'\x00\x00\x00' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT
    assert B._BOUND is None
    assert B._PARTIAL_ALIGNMENT is None

def test_bytes_limited_attributes():
    B = prophy.bytes(bound = "a_len", size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT
    assert "a_len" == B._BOUND
    assert B._PARTIAL_ALIGNMENT is None

def test_bytes_bound_attributes():
    B = prophy.bytes(bound = "a_len")

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT
    assert "a_len" == B._BOUND
    assert B._PARTIAL_ALIGNMENT is None

def test_bytes_greedy_attributes():
    B = prophy.bytes()

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert True == B._UNLIMITED
    assert '' == B._DEFAULT
    assert False == B._OPTIONAL
    assert 1 == B._ALIGNMENT
    assert None == B._BOUND
    assert B._PARTIAL_ALIGNMENT is None

def test_array_static_attributes():
    A = prophy.array(prophy.u16, size = 3)

    assert 6 == A._SIZE
    assert False == A._DYNAMIC
    assert False == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT
    assert None == A._BOUND
    assert A._PARTIAL_ALIGNMENT is None

def test_array_limited_attributes():
    A = prophy.array(prophy.u16, bound = "a_len", size = 3)

    assert 6 == A._SIZE
    assert False == A._DYNAMIC
    assert False == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT
    assert "a_len" == A._BOUND
    assert A._PARTIAL_ALIGNMENT is None

def test_array_bound_attributes():
    A = prophy.array(prophy.u16, bound = "a_len")

    assert 0 == A._SIZE
    assert True == A._DYNAMIC
    assert False == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT
    assert "a_len" == A._BOUND
    assert A._PARTIAL_ALIGNMENT is None

def test_array_greedy_attributes():
    A = prophy.array(prophy.u16)

    assert 0 == A._SIZE
    assert True == A._DYNAMIC
    assert True == A._UNLIMITED
    assert False == A._OPTIONAL
    assert 2 == A._ALIGNMENT
    assert None == A._BOUND
    assert A._PARTIAL_ALIGNMENT is None

def test_container_len_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.bytes(bound = "a_len")),
                       ("b_len", prophy.u8),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]

    assert ["a", "a_len", "b", "b_len"] == [tp._BOUND for _, tp, _, _ in S._descriptor]

def test_struct_static_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
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
    assert S._BOUND is None
    assert S._PARTIAL_ALIGNMENT is None

    class S1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", S),
                       ("b_len", prophy.u8),
                       ("b", prophy.array(S, bound = "b_len", size = 3))]

    assert 61 == S1._SIZE
    assert False == S1._DYNAMIC
    assert False == S1._UNLIMITED
    assert False == S1._OPTIONAL
    assert 1 == S1._ALIGNMENT
    assert None == S1._BOUND

def test_struct_with_optional_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u32)]
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]
    class O(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.optional(prophy.u32)),
                       ("b", prophy.optional(S)),
                       ("c", prophy.optional(U))]

    assert 28 == O._SIZE
    assert False == O._DYNAMIC
    assert False == O._UNLIMITED
    assert False == O._OPTIONAL
    assert 4 == O._ALIGNMENT
    assert None == O._BOUND

def test_struct_dynamic_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len"))]

    assert 1 == S1._SIZE
    assert True == S1._DYNAMIC
    assert False == S1._UNLIMITED
    assert False == S1._OPTIONAL
    assert 1 == S1._ALIGNMENT

    class S2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(S, bound = "a_len"))]

    assert 1 == S2._SIZE
    assert True == S2._DYNAMIC
    assert False == S2._UNLIMITED
    assert False == S2._OPTIONAL
    assert 1 == S2._ALIGNMENT

    class S3(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", S1),
                       ("b", S2)]

    assert 2 == S3._SIZE
    assert True == S3._DYNAMIC
    assert False == S3._UNLIMITED
    assert False == S3._OPTIONAL
    assert 1 == S3._ALIGNMENT

def test_struct_unlimited_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.bytes())]

    assert 0 == S1._SIZE
    assert True == S1._DYNAMIC
    assert True == S1._UNLIMITED
    assert False == S1._OPTIONAL
    assert 1 == S._ALIGNMENT

    class S2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.array(prophy.u8))]

    assert 0 == S2._SIZE
    assert True == S2._DYNAMIC
    assert True == S2._UNLIMITED
    assert False == S2._OPTIONAL
    assert 1 == S2._ALIGNMENT

    class S3(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", S2)]

    assert 0 == S3._SIZE
    assert True == S3._DYNAMIC
    assert True == S3._UNLIMITED
    assert False == S3._OPTIONAL
    assert 1 == S3._ALIGNMENT

def test_struct_padded():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.u32),
                       ("c", prophy.u64)]

    assert 8 == S._ALIGNMENT
    assert 16 == S._SIZE

    class S2(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u32),
                       ("b", S)]

    assert 8 == S2._ALIGNMENT
    assert 24 == S2._SIZE

    class S3(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u32),
                       ("b", prophy.u8)]

    assert 4 == S3._ALIGNMENT
    assert 8 == S3._SIZE

    class S4(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.array(prophy.u8, size = 7)),
                       ("b", prophy.u32)]

    assert 4 == S4._ALIGNMENT
    assert 12 == S4._SIZE

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    class S5(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8),
                       ("b", U),
                       ("c", prophy.u8)]

    assert 4 == S5._ALIGNMENT
    assert 16 == S5._SIZE

def test_struct_partially_padded():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u8),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y", prophy.u32),
                       ("z", prophy.u64)]

    assert X._ALIGNMENT == 8
    assert [tp._PARTIAL_ALIGNMENT for _, tp, _, _ in X._descriptor] == [None, 8, None, None]

    class Y(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u8),
                       ("x", prophy.array(prophy.u8, bound = "x_len")),
                       ("y_len", prophy.u32),
                       ("y", prophy.array(prophy.u8, bound = "y_len")),
                       ("z", prophy.u64)]

    assert Y._ALIGNMENT == 8
    assert [tp._PARTIAL_ALIGNMENT for _, tp, _, _ in Y._descriptor] == [None, 4, None, 8, None]

def test_bytes_partially_padded():
    class Y(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x_len", prophy.u8),
                       ("x", prophy.bytes(bound = "x_len")),
                       ("y_len", prophy.u32),
                       ("y", prophy.bytes(bound = "y_len")),
                       ("z", prophy.u64)]

    assert Y._ALIGNMENT == 8
    assert [tp._PARTIAL_ALIGNMENT for _, tp, _, _ in Y._descriptor] == [None, 4, None, 8, None]

def test_empty_struct():
    class E(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = []

    assert 0 == E._SIZE
    assert False == E._DYNAMIC
    assert False == E._UNLIMITED
    assert False == E._OPTIONAL
    assert 1 == E._ALIGNMENT
    assert None == E._BOUND

def test_union_attributes():
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    assert 8 == U._SIZE
    assert False == U._DYNAMIC
    assert False == U._UNLIMITED
    assert False == U._OPTIONAL
    assert 4 == U._ALIGNMENT
    assert U._BOUND is None
    assert U._PARTIAL_ALIGNMENT is None

def test_union_with_discriminator_padding_attributes():
    class U1(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a1", prophy.u8, 0)]
    class U2(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a2", prophy.u64, 0)]

    assert 8 == U1._SIZE
    assert 4 == U1._ALIGNMENT
    assert 16 == U2._SIZE
    assert 8 == U2._ALIGNMENT
