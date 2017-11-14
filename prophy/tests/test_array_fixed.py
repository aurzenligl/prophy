import prophy
import pytest

@pytest.fixture(scope = 'session')
def X():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.u32)]
    return X

@pytest.fixture(scope = 'session')
def FixedScalarArray():
    class FixedScalarArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.array(prophy.u32, size = 2))]

    return FixedScalarArray

@pytest.fixture(scope = 'session')
def FixedCompositeArray(X):
    class FixedCompositeArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.array(X, size = 2))]
    return FixedCompositeArray

def test_base_array_operators():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('values', prophy.array(prophy.i16, size = 4))]

    x = X()
    x.values[0] = 123
    x.values[2] = 4
    x.values[3] = -1

    with pytest.raises(TypeError) as err:
        set([x.values])
    assert "unhashable" in str(err.value)

    assert len(x.values) == 4
    assert repr(x.values) == '[123, 0, 4, -1]'
    x.values.sort()
    assert x.values == [-1, 0, 4, 123]

def test_fixed_scalar_array_assignment(FixedScalarArray):
    x = FixedScalarArray()
    assert x.value[:] == [0, 0]
    x.value[0] = 1
    x.value[1] = 2
    assert x.value[:] == [1, 2]
    x.value[:] = [6, 7]
    assert x.value[:] == [6, 7]
    x.value[slice(0, 2)] = [6, 7]
    assert x.value[:] == [6, 7]

    with pytest.raises(Exception):
        del x.value[0]
    with pytest.raises(Exception):
        x.value.no_such_attribute
    with pytest.raises(Exception):
        x.value.no_such_attribute = 10
    with pytest.raises(Exception):
        x.value = 10
    with pytest.raises(Exception):
        x.value[:] = 10
    with pytest.raises(Exception):
        x.value[:] = (10,)
    with pytest.raises(Exception):
        x.value[0] = "will fail type check"
    with pytest.raises(Exception):
        x.value[0] = -1

    y = FixedScalarArray()
    y.value[:] = [1, 2]
    y.copy_from(x)
    assert y.value[:] == [6, 7]

def test_fixed_scalar_array_operators(FixedScalarArray):
    x = FixedScalarArray()
    y = FixedScalarArray()
    assert x.value == x.value
    x.value[0] = 23
    assert x.value != y.value
    y.value[0] = 23
    assert x.value == y.value

def test_fixed_scalar_array_print(FixedScalarArray):
    x = FixedScalarArray()
    x.value[:] = [1, 2]
    assert str(x) == ("value: 1\n"
                      "value: 2\n")

def test_fixed_scalar_array_encode(FixedScalarArray):
    x = FixedScalarArray()
    x.value[:] = [1, 2]
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x02"

def test_fixed_scalar_array_decode(FixedScalarArray):
    x = FixedScalarArray()
    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x02", ">")
    assert x.value[:] == [1, 2]

def test_fixed_scalar_array_exception():
    class D(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len"))]

    class U(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a", prophy.array(prophy.u8))]

    with pytest.raises(Exception) as e:
        prophy.array(D, size = 2)
    assert "static/limited array of dynamic type not allowed" == str(e.value)

    with pytest.raises(Exception) as e:
        prophy.array(U, size = 2)
    assert "static/limited array of dynamic type not allowed" == str(e.value)

    with pytest.raises(Exception) as e:
        prophy.array(D, bound = "a_len", size = 2)
    assert "static/limited array of dynamic type not allowed" == str(e.value)

    with pytest.raises(Exception) as e:
        prophy.array(U, bound = "a_len", size = 2)
    assert "static/limited array of dynamic type not allowed" == str(e.value)

def test_fixed_composite_array_assignment(FixedCompositeArray):
    x = FixedCompositeArray()
    assert len(x.value) == 2
    assert x.value[0].x == 0
    assert x.value[1].x == 0
    x.value[0].x = 1
    assert x.value[0].x == 1
    x.value[1].x = 2
    assert x.value[1].x == 2

    y = FixedCompositeArray()
    y.value[0].x = 10
    y.value[1].x = 11
    y.copy_from(x)
    assert y.value[0].x == 1
    assert y.value[1].x == 2

    assert x.value == x.value

def test_fixed_composite_array_print(FixedCompositeArray):
    x = FixedCompositeArray()
    x.value[0].x = 1
    x.value[1].x = 2
    assert str(x) == ("value {\n"
                      "  x: 1\n"
                      "}\n"
                      "value {\n"
                      "  x: 2\n"
                      "}\n")

def test_fixed_composite_array_encode(FixedCompositeArray):
    x = FixedCompositeArray()
    x.value[0].x = 1
    x.value[1].x = 2
    assert x.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x02"

def test_fixed_composite_array_decode(FixedCompositeArray):
    x = FixedCompositeArray()
    x.decode(b"\x00\x00\x00\x01\x00\x00\x00\x02", ">")
    assert x.value[0].x == 1
    assert x.value[1].x == 2

def test_fixed_array_with_enum():
    class E(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]

    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.array(E, size = 3))]

    x = A()

    x.encode(">")

def test_fixed_array_decode_exception():
    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len", size = 3))]

    with pytest.raises(Exception) as e:
        A().decode(b"\x00", ">")
    assert "A: too few bytes to decode array" == str(e.value)

def test_fixed_array_decode_size_over_255():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.array(prophy.u8, size = 300))]

    x = X()
    x.decode(b'\x01' * 300, '<')
    assert len(x.x) == 300

def test_fixed_array_decode_multiple_scalar_arrays():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('x', prophy.array(prophy.u8, size = 1)),
                       ('y', prophy.array(prophy.u8, size = 1)),
                       ('z', prophy.array(prophy.u8, size = 1))]
    x = X()
    x.decode(b'\x00\x00\x00', '<')

def test_fixed_array_decode_multiple_composite_arrays():
    class Y(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('x', prophy.u8)]

    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('x', prophy.array(Y, size = 1)),
                       ('y', prophy.array(Y, size = 1)),
                       ('z', prophy.array(Y, size = 1))]

    x = X()
    x.decode(b'\x00\x00\x00', '<')
