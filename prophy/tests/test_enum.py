import prophy
import pytest

@pytest.fixture(scope = 'session')
def Enumeration():
    class Enumeration(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("Enumeration_One", 1),
                        ("Enumeration_Two", 2),
                        ("Enumeration_Three", 3)]
    return Enumeration

@pytest.fixture(scope = 'session')
def Enumeration8():
    class Enumeration8(prophy.enum8):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("Enumeration_One", 1),
                        ("Enumeration_Two", 2),
                        ("Enumeration_Three", 3)]
    return Enumeration8

@pytest.fixture(scope = 'session')
def Enum(Enumeration):
    class Enum(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", Enumeration)]
    return Enum

@pytest.fixture(scope = 'session')
def Enum8(Enumeration8):
    class Enum8(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", Enumeration8)]
    return Enum8

@pytest.fixture(scope = 'session')
def EnumFixedArray(Enumeration):
    class EnumFixedArray(prophy.struct_packed):
         __metaclass__ = prophy.struct_generator
         _descriptor = [("value", prophy.array(Enumeration, size = 2))]
    return EnumFixedArray

@pytest.fixture(scope = 'session')
def EnumBoundArray(Enumeration):
    class EnumBoundArray(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.array(Enumeration, bound = "value_len"))]
    return EnumBoundArray

def test_enum_assignment(Enum):
    x = Enum()
    assert x.value == 1
    x.value = "Enumeration_Two"
    assert x.value == 2
    x.value = 3
    assert x.value == 3

    with pytest.raises(prophy.ProphyError):
        x.value = "Enumeration_Four"
    with pytest.raises(prophy.ProphyError):
        x.value = 4

    y = Enum()
    y.copy_from(x)
    assert y.value == 3

def test_enum_encoding(Enum):
    x = Enum()
    x.value = 2
    assert str(x) == "value: Enumeration_Two\n"

    assert x.encode(">") == "\x00\x00\x00\x02"

    x.decode("\x00\x00\x00\x03", ">")
    assert x.value == 3

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x00\x00\x00\x09", ">")
    assert 'unknown enumerator value' in e.value.message

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x00\x00\x01", ">")
    assert 'too few bytes to decode integer' in e.value.message

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x00\x00\x00\x01\x01", ">")
    assert 'not all bytes read' in e.value.message

def test_enum_exceptions():
    with pytest.raises(Exception):
        class NoEnumerators(prophy.enum):
            __metaclass__ = prophy.enum_generator
    with pytest.raises(Exception):
        class NamesOverlapping(prophy.enum):
            __metaclass__ = prophy.enum_generator
            _enumerators = [("NamesOverlapping_Overlap", 1),
                            ("NamesOverlapping_Overlap", 2)]
    with pytest.raises(Exception):
        class ValueOutOfBounds(prophy.enum):
            __metaclass__ = prophy.enum_generator
            _enumerators = [("OutOfBounds", 0xFFFFFFFF + 1)]

def test_enum8_encoding(Enum8):
    x = Enum8()
    x.value = 2
    assert str(x) == "value: Enumeration_Two\n"

    x.value = 2
    assert x.encode(">") == "\x02"

    x.decode("\x02", ">")
    assert x.value == 2

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x09", ">")
    assert 'unknown enumerator value' in e.value.message

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("", ">")
    assert 'too few bytes to decode integer' in e.value.message

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x01\x01", ">")
    assert 'not all bytes read' in e.value.message

def test_enum_with_overlapping_values():
    class ValuesOverlapping(prophy.enum8):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("ValuesOverlapping_First", 42),
                        ("ValuesOverlapping_Second", 42)]
    class X(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", ValuesOverlapping)]

    x = X()
    assert 42 == x.x
    assert "x: ValuesOverlapping_Second\n" == str(x)

    x.x = "ValuesOverlapping_Second"
    assert 42 == x.x
    x.x = "ValuesOverlapping_First"
    assert 42 == x.x
    assert "x: ValuesOverlapping_Second\n" == str(x)

def test_enum_fixed_array_assignment(EnumFixedArray):
    x = EnumFixedArray()
    assert x.value == [1, 1]
    assert x.value[0] == 1
    assert x.value[1] == 1
    x.value[0] = 2
    x.value[1] = "Enumeration_Two"
    assert x.value == [2, 2]

    y = EnumFixedArray()
    y.value[:] = [3, 3]
    y.copy_from(x)
    assert y.value == [2, 2]

def test_enum_fixed_array_encoding(EnumFixedArray):
    x = EnumFixedArray()
    x.value[:] = [2, 2]
    assert str(x) == ("value: Enumeration_Two\n"
                      "value: Enumeration_Two\n")

    x.value[:] = [2, 2]
    assert x.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x02"

    x.decode("\x00\x00\x00\x02\x00\x00\x00\x02", ">")
    assert x.value[0] == 2
    assert x.value[1] == 2

def test_enum_bound_array_assignment(EnumBoundArray):
    x = EnumBoundArray()
    assert x.value == []
    x.value[:] = [1, "Enumeration_One"]
    assert x.value == [1, 1]
    assert x.value[0] == 1
    assert x.value[1] == 1
    x.value[0] = 2
    x.value[1] = "Enumeration_Two"
    assert x.value == [2, 2]

def test_enum_bound_array_encoding(EnumBoundArray):
    x = EnumBoundArray()
    x.value[:] = [2, 2]
    assert str(x) == ("value: Enumeration_Two\n"
                      "value: Enumeration_Two\n")

    x.value[:] = [2, 2]
    assert x.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02"

    x.decode("\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02", ">")
    assert x.value[0] == 2
    assert x.value[1] == 2

def test_enum_with_0xFFFFFFFF_value():
    class Enum(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [('Enum_Infinity', 0xFFFFFFFF)]
    class Enclosing(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", Enum)]

    assert Enclosing().value == 0xFFFFFFFF

def test_enum_access_to_members():
    class E(prophy.enum):
        __metaclass__ = prophy.enum_generator
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]

    x = E()

    with pytest.raises(Exception) as e:
        x.not_available = 102
    assert "has no attribute" in e.value.message

    class S(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", E),
                       ("b", prophy.array(E))]

    y = S()
    y.b[:] = [1, 1]
    y.b[1] = 1
    y.b.append(1)

    assert y.a.__class__ == E
    assert y.b[0].__class__ == E
    assert y.b[1].__class__ == E
    assert y.b[2].__class__ == E

    assert y.a.name == "E_1"
    assert y.a.number == 1

    y.decode('\x00\x00\x00\x01\x00\x00\x00\x01', '>')
    assert y.a.__class__ == E
    assert y.b[0].__class__ == E

    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", E, 0)]

    z = U()

    assert z.a.__class__ == E
