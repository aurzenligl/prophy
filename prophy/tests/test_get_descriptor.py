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



def test_kind_constant():

    with pytest.raises(ValueError) as e:
        prophy.kind.kind.STRUCT = 10
    assert "Cannot assign to a constant." == str(e.value)


def test_struct_instance_get_descriptor(DeeplyNestedStruct,NestedStruct,Struct):

  fields = DeeplyNestedStruct().get_descriptor()

  ref = [['m', prophy.kind.kind.STRUCT, NestedStruct],
         ['n', prophy.kind.kind.STRUCT, Struct],
         ['o', prophy.kind.kind.INT, prophy.u32]]

  for idx,f in enumerate(fields):
    assert f.name == ref[idx][0]
    assert f.kind == ref[idx][1]
    assert f.type_ == ref[idx][2]

def test_struct_type_get_descriptor(DeeplyNestedStruct,NestedStruct,Struct):

  fields = DeeplyNestedStruct.get_descriptor()

  ref = [['m', prophy.kind.kind.STRUCT, NestedStruct],
         ['n', prophy.kind.kind.STRUCT, Struct],
         ['o', prophy.kind.kind.INT, prophy.u32]]

  for idx,f in enumerate(fields):
    assert f.name == ref[idx][0]
    assert f.kind == ref[idx][1]
    assert f.type_ == ref[idx][2]


def test_union_instance_get_discriminated(Union,Struct):

  x = Union()

  ref = [['a', prophy.kind.kind.INT, prophy.u16],
         ['b', prophy.kind.kind.INT, prophy.u32],
         ['c', prophy.kind.kind.STRUCT, Struct]]

  for disc in range(3):
    x.discriminator = disc
    field = x.get_discriminated()
    assert field.name  == ref[disc][0]
    assert field.kind  == ref[disc][1]
    assert field.type_ == ref[disc][2]


def test_union_type_get_descriptor(Union,Struct):

  fields = Union.get_descriptor()

  ref = [['a', prophy.kind.kind.INT, prophy.u16],
         ['b', prophy.kind.kind.INT, prophy.u32],
         ['c', prophy.kind.kind.STRUCT, Struct]]

  for idx,f in enumerate(fields):
    assert f.name   == ref[idx][0]
    assert f.kind   == ref[idx][1]
    assert f.type_  == ref[idx][2]