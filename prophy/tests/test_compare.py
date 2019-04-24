import prophy

import pytest


def get_integer_class1(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", _type)]
    return X


def get_optional_class1(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", prophy.optional(_type))]
    return X


def get_array_class1(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", prophy.array(_type))]
    return X


def get_array_class2(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", prophy.array(_type, size=4))]
    return X


def get_array_class3(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.array(_type, size=4))]
    return X


def get_array_bound_class1(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(_type, bound="len"))]
    return X


def get_array_bound_class2(_type):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("len", prophy.i32),
                       ("value", prophy.array(_type, bound="len"))]
    return X


def get_enum_class1():
    class X(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [
            ("x", 1),
            ("y", 2),
        ]
    return X


def get_enum_class2():
    class X(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [
            ("x", 1),
            ("y", 3),
        ]
    return X


def get_enum_class3():
    class X(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [
            ("x", 1),
            ("z", 3),
        ]
    return X


def get_fixed_bytes():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.bytes(size=5))]
    return X


def get_bound_bytes():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.bytes(bound="value_len"))]
    return X


def get_shift_bound_bytes():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u8),
                       ("value", prophy.bytes(bound="value_len", shift=2))]
    return X


def get_limited_bytes():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.bytes(size=5, bound="value_len"))]
    return X


def get_greedy_bytes():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.bytes())]
    return X


@pytest.mark.parametrize('_type', [
    prophy.i8,
    prophy.i16,
    prophy.i32,
    prophy.i64,
    prophy.u8,
    prophy.u16,
    prophy.u32,
    prophy.u64,
    prophy.r32
])
def test_compare_descriptors_scalars(_type):
    x = get_integer_class1(_type)
    y = get_integer_class1(_type)
    assert x == y


@pytest.mark.parametrize('_type', [
    prophy.i8,
    prophy.i16,
    prophy.i32,
    prophy.i64,
    prophy.u8,
    prophy.u16,
    prophy.u32,
    prophy.u64,
    prophy.r32
])
def test_compare_descriptors_arrays(_type):
    a, b = get_array_bound_class1(_type), get_array_bound_class1(_type)
    c, d = get_array_bound_class2(_type), get_array_bound_class2(_type)
    e, f = get_array_class1(_type), get_array_class1(_type)
    g, h = get_array_class2(_type), get_array_class2(_type)
    i, j = get_array_class3(_type), get_array_class3(_type)

    assert a == b
    assert c == d
    assert e == f
    assert g == h
    assert i == j
    assert a != c
    assert a != e
    assert a != g
    assert a != i
    assert c != e
    assert c != g
    assert c != i
    assert e != g
    assert e != i
    assert g != i


@pytest.mark.parametrize('_type', [
    prophy.i8,
    prophy.i16,
    prophy.i32,
    prophy.i64,
    prophy.u8,
    prophy.u16,
    prophy.u32,
    prophy.u64,
    prophy.r32
])
def test_compare_descriptors_optional(_type):
    x = get_optional_class1(_type)
    y = get_optional_class1(_type)
    assert x == y


def test_compare_enum():
    x, y = get_enum_class1(), get_enum_class1()
    z = get_enum_class2()
    w = get_enum_class3()
    assert x == y
    assert x != z
    assert x != w
    assert z != w


def test_compare_bytes():
    a, b = get_fixed_bytes(), get_fixed_bytes()
    c, d = get_bound_bytes(), get_bound_bytes()
    e, f = get_greedy_bytes(), get_greedy_bytes()
    g, h = get_limited_bytes(), get_limited_bytes()
    assert a == b
    assert c == d
    assert e == f
    assert g == h
    assert a != c
    assert a != e
    assert a != g
    assert c != e
    assert e != g
