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
    assert tp._DYNAMIC is False
    assert tp._UNLIMITED is False
    assert tp._DEFAULT == 0
    assert tp._OPTIONAL is False
    assert tp._ALIGNMENT == size
    assert tp._BOUND is None
    assert tp._PARTIAL_ALIGNMENT is None

@pytest.mark.parametrize("tp, size", [
    (prophy.r32, 4),
    (prophy.r64, 8)
])
def test_float_attributes(tp, size):
    assert tp._SIZE == size
    assert tp._DYNAMIC is False
    assert tp._UNLIMITED is False
    assert tp._DEFAULT == 0.0
    assert tp._OPTIONAL is False
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
    assert tp_factory()._DYNAMIC is False
    assert tp_factory()._UNLIMITED is False
    assert tp_factory()._DEFAULT == 1
    assert tp_factory()._OPTIONAL is False
    assert tp_factory()._ALIGNMENT == size
    assert tp_factory()._BOUND is None
    assert tp_factory()._PARTIAL_ALIGNMENT is None

def test_optional_attributes():
    assert prophy.optional(prophy.i8)._SIZE == 1
    assert prophy.optional(prophy.i8)._DYNAMIC is False
    assert prophy.optional(prophy.i8)._UNLIMITED is False
    assert prophy.optional(prophy.i8)._DEFAULT == 0
    assert prophy.optional(prophy.i8)._OPTIONAL
    assert prophy.optional(prophy.i8)._ALIGNMENT == 1
    assert prophy.optional(prophy.i8)._BOUND is None
    assert prophy.optional(prophy.i8)._PARTIAL_ALIGNMENT is None

    assert prophy.optional(prophy.i8)._OPTIONAL_SIZE == 5
    assert prophy.optional(prophy.i8)._OPTIONAL_ALIGNMENT == 4
    assert prophy.optional(prophy.i64)._OPTIONAL_SIZE == 16
    assert prophy.optional(prophy.i64)._OPTIONAL_ALIGNMENT == 8

def test_bytes_static_attributes():
    B = prophy.bytes(size = 3)

    assert B._SIZE == 3
    assert B._DYNAMIC is False
    assert B._UNLIMITED is False
    assert B._DEFAULT == b'\x00\x00\x00'
    assert B._OPTIONAL is False
    assert B._ALIGNMENT == 1
    assert B._BOUND is None
    assert B._PARTIAL_ALIGNMENT is None

def test_bytes_limited_attributes():
    B = prophy.bytes(bound = "a_len", size = 3)

    assert B._SIZE == 3
    assert B._DYNAMIC is False
    assert B._UNLIMITED is False
    assert B._DEFAULT == ''
    assert B._OPTIONAL is False
    assert B._ALIGNMENT == 1
    assert B._BOUND == "a_len"
    assert B._PARTIAL_ALIGNMENT is None

def test_bytes_bound_attributes():
    B = prophy.bytes(bound = "a_len")

    assert B._SIZE == 0
    assert B._DYNAMIC is True
    assert B._UNLIMITED is False
    assert B._DEFAULT == ''
    assert B._OPTIONAL is False
    assert B._ALIGNMENT == 1
    assert B._BOUND == "a_len"
    assert B._PARTIAL_ALIGNMENT is None

def test_bytes_greedy_attributes():
    B = prophy.bytes()

    assert B._SIZE == 0
    assert B._DYNAMIC is True
    assert B._UNLIMITED is True
    assert B._DEFAULT == ''
    assert B._OPTIONAL is False
    assert B._ALIGNMENT == 1
    assert B._BOUND is None
    assert B._PARTIAL_ALIGNMENT is None

def test_array_static_attributes():
    A = prophy.array(prophy.u16, size = 3)

    assert A._SIZE == 6
    assert A._DYNAMIC is False
    assert A._UNLIMITED is False
    assert A._OPTIONAL is False
    assert A._ALIGNMENT == 2
    assert A._BOUND is None
    assert A._PARTIAL_ALIGNMENT is None

def test_array_limited_attributes():
    A = prophy.array(prophy.u16, bound = "a_len", size = 3)

    assert A._SIZE == 6
    assert A._DYNAMIC is False
    assert A._UNLIMITED is False
    assert A._OPTIONAL is False
    assert A._ALIGNMENT == 2
    assert A._BOUND == "a_len"
    assert A._PARTIAL_ALIGNMENT is None

def test_array_bound_attributes():
    A = prophy.array(prophy.u16, bound = "a_len")

    assert A._SIZE == 0
    assert A._DYNAMIC is True
    assert A._UNLIMITED is False
    assert A._OPTIONAL is False
    assert A._ALIGNMENT == 2
    assert A._BOUND == "a_len"
    assert A._PARTIAL_ALIGNMENT is None

def test_array_greedy_attributes():
    A = prophy.array(prophy.u16)

    assert A._SIZE == 0
    assert A._DYNAMIC is True
    assert A._UNLIMITED is True
    assert A._OPTIONAL is False
    assert A._ALIGNMENT == 2
    assert A._BOUND is None
    assert A._PARTIAL_ALIGNMENT is None

def test_array_incorrect_attributes():
    with pytest.raises(prophy.ProphyError) as err:
        prophy.array(prophy.u16, anything = 3)

    assert str(err.value) == "unknown arguments to array field"

def test_array_of_arrays_not_allowed():
    A = prophy.array(prophy.r32)
    with pytest.raises(prophy.ProphyError) as err:
        prophy.array(A, size = 3)

    assert str(err.value) == "array of arrays not allowed"

def test_container_len_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.bytes(bound = "a_len")),
                       ("b_len", prophy.u8),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]

    assert [["a"], "a_len", ["b"], "b_len"] == [tpl[1]._BOUND for tpl in S._descriptor]
    assert ["a_len", "a", "b_len", "b"] == [tpl[0] for tpl in S._descriptor]

def test_ext_sized_array_attributes_1():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sizer", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "sizer")),
                       ("b", prophy.array(prophy.u16, bound = "sizer")),
                       ("c", prophy.array(prophy.u32, bound = "sizer"))]

    assert [["a", "b", "c"], "sizer", "sizer", "sizer"] == [tpl[1]._BOUND for tpl in S._descriptor]
    assert ["sizer", "a", "b", "c"] == [tpl[0] for tpl in S._descriptor]

def test_ext_sized_array_attributes_2():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sz1", prophy.u8),
                       ("sz2", prophy.u8),
                       ("a1", prophy.array(prophy.u8, bound = "sz1")),
                       ("a2", prophy.array(prophy.u16, bound = "sz2")),
                       ("b1", prophy.array(prophy.u32, bound = "sz1")),
                       ("b2", prophy.array(prophy.u32, bound = "sz2"))]

    assert [["a1", "b1"], ["a2", "b2"], "sz1", "sz2", "sz1", "sz2"] == [tpl[1]._BOUND for tpl in S._descriptor]
    assert ["sz1", "sz2", "a1", "a2", "b1", "b2"] == [tpl[0] for tpl in S._descriptor]

def test_struct_static_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8),
                       ("c_len", prophy.u8),
                       ("e_len", prophy.u8),
                       ("b", prophy.bytes(size = 3)),
                       ("c", prophy.bytes(bound = "c_len", size = 3)),
                       ("d", prophy.array(prophy.u8, size = 3)),
                       ("e", prophy.array(prophy.u8, bound = "e_len", size = 3))]

    assert S._SIZE == 15
    assert S._DYNAMIC is False
    assert S._UNLIMITED is False
    assert S._OPTIONAL is False
    assert S._ALIGNMENT == 1
    assert S._BOUND is None
    assert S._PARTIAL_ALIGNMENT is None

    class S1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", S),
                       ("b_len", prophy.u8),
                       ("b", prophy.array(S, bound = "b_len", size = 3))]

    assert S1._SIZE == 61
    assert S1._DYNAMIC is False
    assert S1._UNLIMITED is False
    assert S1._OPTIONAL is False
    assert S1._ALIGNMENT == 1
    assert S1._BOUND is None

def test_struct_with_optional_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u32)]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    class K(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.optional(prophy.u32)),
                       ("b", prophy.optional(S)),
                       ("c", prophy.optional(U))]

    assert K._SIZE == 28
    assert K._DYNAMIC is False
    assert K._UNLIMITED is False
    assert K._OPTIONAL is False
    assert K._ALIGNMENT == 4
    assert K._BOUND is None

def test_struct_dynamic_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len"))]

    assert S1._SIZE == 1
    assert S1._DYNAMIC is True
    assert S1._UNLIMITED is False
    assert S1._OPTIONAL is False
    assert S1._ALIGNMENT == 1

    class S2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(S, bound = "a_len"))]

    assert S2._SIZE == 1
    assert S2._DYNAMIC is True
    assert S2._UNLIMITED is False
    assert S2._OPTIONAL is False
    assert S2._ALIGNMENT == 1

    class S3(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", S1),
                       ("b", S2)]

    assert S3._SIZE == 2
    assert S3._DYNAMIC is True
    assert S3._UNLIMITED is False
    assert S3._OPTIONAL is False
    assert S3._ALIGNMENT == 1

def test_struct_unlimited_attributes():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.u8)]

    class S1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.bytes())]

    assert S1._SIZE == 0
    assert S1._DYNAMIC is True
    assert S1._UNLIMITED is True
    assert S1._OPTIONAL is False
    assert S1._ALIGNMENT == 1

    class S2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.array(prophy.u8))]

    assert S2._SIZE == 0
    assert S2._DYNAMIC is True
    assert S2._UNLIMITED is True
    assert S2._OPTIONAL is False
    assert S2._ALIGNMENT == 1

    class S3(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", S2)]

    assert S3._SIZE == 0
    assert S3._DYNAMIC is True
    assert S3._UNLIMITED is True
    assert S3._OPTIONAL is False
    assert S3._ALIGNMENT == 1

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

    assert E._SIZE == 0
    assert E._DYNAMIC is False
    assert E._UNLIMITED is False
    assert E._OPTIONAL is False
    assert E._ALIGNMENT == 1
    assert E._BOUND is None

def test_union_attributes():
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    assert U._SIZE == 8
    assert U._DYNAMIC is False
    assert U._UNLIMITED is False
    assert U._OPTIONAL is False
    assert U._ALIGNMENT == 4
    assert U._BOUND is None
    assert U._PARTIAL_ALIGNMENT is None

def test_union_with_discriminator_padding_attributes():
    class U1(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a1", prophy.u8, 0)]

    class U2(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a2", prophy.u64, 0)]

    assert U1._SIZE == 8
    assert U1._ALIGNMENT == 4
    assert U2._SIZE == 16
    assert U2._ALIGNMENT == 8

def test_getting_descriptor():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.array(prophy.u32, size = 2))]

    class E(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("E_1", 1)]

    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8),
                       ("b", prophy.bytes(size = 5))]

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1)]

    class Top(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("A", A), ("E", E), ("S", S), ("U", U)]

    t = Top()
    assert len(t.get_descriptor()) == 4
    assert len(t.A.get_descriptor()) == 1
    assert len(t.S.get_descriptor()) == 2

def test_field_descriptor_repr():
    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u8, 0),
                       ("b", prophy.u16, 1),
                       ("c", prophy.u32, 2)]

    descriptors = U.get_descriptor()
    assert list(map(repr, descriptors)) == ["<a, <class 'prophy.scalar.u8'>, ('INT', 0)>",
                                            "<b, <class 'prophy.scalar.u16'>, ('INT', 0)>",
                                            "<c, <class 'prophy.scalar.u32'>, ('INT', 0)>"]
