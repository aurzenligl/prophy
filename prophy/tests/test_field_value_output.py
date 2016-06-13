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



def test_simple_struct_fields(DeeplyNestedStruct):
    x = DeeplyNestedStruct()
    assert x.fields() == ["m.a.x",
                          "m.a.y",
                          "m.b.x",
                          "m.b.y",
                          "n.x",
                          "n.y",
                          "o"]

def test_simple_struct_values(DeeplyNestedStruct):
    x = DeeplyNestedStruct()
    x.m.a.x = 0xbeefdead
    x.m.a.y = 0xdeadbeef
    x.n.x = 71551
    x.o = 1337

    res = cmp(x.values(),{"m.a.x":0xbeefdead,
                          "m.a.y":0xdeadbeef,
                          "m.b.x":0,
                          "m.b.y":0,
                          "n.x"  :71551,
                          "n.y"  :0,
                          "o"    :1337})
    assert res == 0


def test_simple_union_fields(Union):
    x = Union()
    x.discriminator = 2
    print(x)
    assert x.fields() == ["c.x","c.y"]

def test_simple_union_values(Union):
    x = Union()
    x.discriminator = 1
    x.b = 0xdeadbeef

    res = cmp(x.values(),{"b": 0xdeadbeef})
    assert res == 0


def test_compicated_message_fields(ComplicatedStruct):

    msg = ComplicatedStruct()
    msg.d[0].discriminator = 1
    msg.d[1].discriminator = 2

    assert msg.fields() == [  "a.a.x",
                              "a.a.y",
                              "a.b.x",
                              "a.b.y",
                              "b",
                              "c[0].x",
                              "c[0].y",
                              "c[1].x",
                              "c[1].y",
                              "d[0].b",
                              "d[1].c.x",
                              "d[1].c.y",]


def test_complicated_message_values(ComplicatedStruct):

    msg = ComplicatedStruct()

    msg.a.a.x  = 1337
    msg.b      = 0xdeadbeef
    msg.c[1].x = 0xbeef
    msg.a.b.y  = 0xf007ba11
    msg.d[0].discriminator = 1
    msg.d[1].discriminator = 2
    msg.d[0].b   = 0xbeef
    msg.d[1].c.y = 0xdead

    res = cmp(msg.values(), { "a.a.x"   : 1337,
			                  "a.a.y"   : 0,
			                  "a.b.x"   : 0,
			                  "a.b.y"   : 4027038225,
			                  "b"       : 3735928559,
			                  "c[0].x"  : 0,
			                  "c[0].y"  : 0,
			                  "c[1].x"  : 48879,
			                  "c[1].y"  : 0,
			                  "d[0].b"  : 48879,
			                  "d[1].c.x": 0,
			                  "d[1].c.y": 57005})
    assert res == 0