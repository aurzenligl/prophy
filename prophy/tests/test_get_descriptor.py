import prophy
import pytest

@pytest.fixture(scope = 'session')
def Struct():
    class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.u32),
                       ("y", prophy.u32)]
    return Struct

@pytest.fixture(scope = 'session')
def Union(Struct):
    class Union(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [("a", prophy.u16, 0),
                       ("b", prophy.u32, 1),
                       ("c", Struct, 2)]
    return Union

@pytest.fixture(scope = 'session')
def NestedStruct(Struct):
    class NestedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", Struct),
                       ("b", Struct)]
    return NestedStruct

@pytest.fixture(scope = 'session')
def DeeplyNestedStruct(NestedStruct, Struct):
    class DeeplyNestedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("m", NestedStruct),
                       ("n", Struct),
                       ("o", prophy.u32)]
    return DeeplyNestedStruct

@pytest.fixture(scope = 'session')
def ComplicatedStruct(NestedStruct, Struct, Union):
    class ComplicatedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", NestedStruct),
                       ("b", prophy.u32),
                       ("c", prophy.array(Struct, size = 2)),
                       ("d", prophy.array(Union, size = 2))]
    return ComplicatedStruct

def desc_to_tuples(desc):
    return [(fdesc.name, fdesc.kind, fdesc.type) for fdesc in desc]

def disc_to_tuple(unionObj, disc):
    unionObj.discriminator = disc
    fields = unionObj.get_discriminated()
    return (fields.name, fields.kind, fields.type)

def test_struct_type_get_descriptor(DeeplyNestedStruct, NestedStruct, Struct):
    assert desc_to_tuples(DeeplyNestedStruct.get_descriptor()) == [
        ('m', prophy.kind.STRUCT, NestedStruct),
        ('n', prophy.kind.STRUCT, Struct),
        ('o', prophy.kind.INT, prophy.u32)
    ]

def test_struct_instance_get_descriptor(DeeplyNestedStruct, NestedStruct, Struct):
    assert desc_to_tuples(DeeplyNestedStruct().get_descriptor()) == [
        ('m', prophy.kind.STRUCT, NestedStruct),
        ('n', prophy.kind.STRUCT, Struct),
        ('o', prophy.kind.INT, prophy.u32)
    ]

def test_union_type_get_descriptor(Union, Struct):
    assert desc_to_tuples(Union.get_descriptor()) == [
        ('a', prophy.kind.INT, prophy.u16),
        ('b', prophy.kind.INT, prophy.u32),
        ('c', prophy.kind.STRUCT, Struct)
    ]

def test_union_instance_get_discriminated(Union, Struct):
    x = Union()
    assert [disc_to_tuple(x, disc) for disc in range(3)] == [
        ('a', prophy.kind.INT, prophy.u16),
        ('b', prophy.kind.INT, prophy.u32),
        ('c', prophy.kind.STRUCT, Struct)
    ]
