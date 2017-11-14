import prophy
import pytest

@pytest.fixture(scope = 'session')
def Enumeration():
    class Enumeration(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("Enumeration_One", 1),
                        ("Enumeration_Two", 2),
                        ("Enumeration_Three", 3)]
    return Enumeration

@pytest.fixture(scope = 'session')
def Enumeration8():
    class Enumeration8(prophy.with_metaclass(prophy.enum_generator, prophy.enum8)):
        _enumerators = [("Enumeration_One", 1),
                        ("Enumeration_Two", 2),
                        ("Enumeration_Three", 3)]
    return Enumeration8

@pytest.fixture(scope = 'session')
def Enum(Enumeration):
    class Enum(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", Enumeration)]
    return Enum

@pytest.fixture(scope = 'session')
def Enum8(Enumeration8):
    class Enum8(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", Enumeration8)]
    return Enum8

@pytest.fixture(scope = 'session')
def EnumFixedArray(Enumeration):
    class EnumFixedArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.array(Enumeration, size = 2))]
    return EnumFixedArray

@pytest.fixture(scope = 'session')
def EnumBoundArray(Enumeration):
    class EnumBoundArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.array(Enumeration, bound = "value_len"))]
    return EnumBoundArray

def test_enum_dictionaties(Enumeration):
    assert Enumeration._name_to_int == {'Enumeration_One': 1, 'Enumeration_Two': 2, 'Enumeration_Three': 3}
    assert Enumeration._int_to_name == {1: 'Enumeration_One', 2: 'Enumeration_Two', 3: 'Enumeration_Three'}

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

    assert x.encode(">") == b"\x00\x00\x00\x02"

    x.decode(b"\x00\x00\x00\x03", ">")
    assert x.value == 3

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x00\x00\x00\x09", ">")
    assert 'unknown enumerator Enumeration value' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x00\x00\x01", ">")
    assert 'too few bytes to decode integer' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x00\x00\x00\x01\x01", ">")
    assert 'not all bytes of Enum read' in str(e.value)

def test_enum_exceptions():
    with pytest.raises(Exception):
        class NoEnumerators(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
            pass
    with pytest.raises(Exception):
        class NamesOverlapping(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
            _enumerators = [("NamesOverlapping_Overlap", 1),
                            ("NamesOverlapping_Overlap", 2)]
    with pytest.raises(Exception):
        class ValueOutOfBounds(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
            _enumerators = [("OutOfBounds", 0xFFFFFFFF + 1)]

def test_enum8_encoding(Enum8):
    x = Enum8()
    x.value = 2
    assert str(x) == "value: Enumeration_Two\n"

    x.value = 2
    assert x.encode(">") == b"\x02"

    x.decode(b"\x02", ">")
    assert x.value == 2

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x09", ">")
    assert 'unknown enumerator Enumeration8 value' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"", ">")
    assert 'too few bytes to decode integer' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x01\x01", ">")
    assert 'not all bytes of Enum8 read' in str(e.value)

def test_enum_with_overlapping_values():
    class ValuesOverlapping(prophy.with_metaclass(prophy.enum_generator, prophy.enum8)):
        _enumerators = [("ValuesOverlapping_First", 42),
                        ("ValuesOverlapping_Second", 42)]

    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
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
    assert x.encode(">") == b"\x00\x00\x00\x02\x00\x00\x00\x02"

    x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x02", ">")
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
    assert x.encode(">") == b"\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02"

    x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02", ">")
    assert x.value[0] == 2
    assert x.value[1] == 2

def test_enum_with_0xFFFFFFFF_value():
    class Enum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [('Enum_Infinity', 0xFFFFFFFF)]

    class Enclosing(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", Enum)]

    assert Enclosing().value == 0xFFFFFFFF

def test_enum_access_to_members():
    class E(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]

    x = E()

    with pytest.raises(Exception) as e:
        x.not_available = 102
    assert "has no attribute" in str(e.value)

    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
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

    y.decode(b'\x00\x00\x00\x01\x00\x00\x00\x01', '>')
    assert y.a.__class__ == E
    assert y.b[0].__class__ == E

    class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", E, 0)]

    z = U()

    assert z.a.__class__ == E
