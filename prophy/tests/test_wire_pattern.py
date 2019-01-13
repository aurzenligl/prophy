import pytest

import prophy


@pytest.fixture
def Struct():
    class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.i16),
                       ("y", prophy.u8)]

    return Struct


@pytest.fixture
def NestedStruct(Struct):
    class NestedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("structure", Struct),
                       ("scalar", prophy.i64)]

    return NestedStruct


@pytest.fixture
def DeeplyNestedStruct(NestedStruct, Struct):
    class DeeplyNestedStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("m", NestedStruct),
                       ("n", Struct),
                       ("o", prophy.u32)]

    return DeeplyNestedStruct


@pytest.fixture
def WiteStampSample(DeeplyNestedStruct, Struct):
    class Nest(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [
            ("scalar", prophy.i16),
            ("composite", Struct),
        ]

    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [
            ("integer", prophy.u16),
            ("a_len", prophy.u16),
            ("bound", prophy.array(Nest, bound="a_len")),
            ("fixed", prophy.array(Nest, size=2)),
            ("limitted", prophy.array(Nest, bound="a_len", size=2)),
            ("c_len", prophy.u8),
            ("bound_scalar", prophy.array(prophy.i64, bound="c_len")),
            ("fixed_scalar", prophy.array(prophy.i16, size=2)),
            ("nested", DeeplyNestedStruct),
            ("b", prophy.bytes())
        ]

    return A
