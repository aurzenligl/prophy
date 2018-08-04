import prophy
import pytest


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


def test_wire_pattern(WiteStampSample):
    result = list(WiteStampSample.wire_pattern())
    """
        Thats just a temporary check of current functionality.
    """
    assert result == [
        ('.integer', 'u16', 2),
        ('.a_len (sizer)', 'u16', 2),
        ('.bound[@a_len].scalar', 'i16', 2),
        ('.bound[@a_len].composite.x', 'i16', 2),
        ('.bound[@a_len].composite.y', 'u8', 1),
        ('.bound[@a_len].composite.y.:final_padding', '<Pd1>', 1),
        ('.bound.:partial_padding', '<Pd6>', 6),
        ('.fixed[0].scalar', 'i16', 2),
        ('.fixed[0].composite.x', 'i16', 2),
        ('.fixed[0].composite.y', 'u8', 1),
        ('.fixed[0].composite.y.:final_padding', '<Pd1>', 1),
        ('.fixed[1].scalar', 'i16', 2),
        ('.fixed[1].composite.x', 'i16', 2),
        ('.fixed[1].composite.y', 'u8', 1),
        ('.fixed[1].composite.y.:final_padding', '<Pd1>', 1),
        ('.limitted[0].scalar', 'i16', 2),
        ('.limitted[0].composite.x', 'i16', 2),
        ('.limitted[0].composite.y', 'u8', 1),
        ('.limitted[0].composite.y.:final_padding', '<Pd1>', 1),
        ('.limitted[1].scalar', 'i16', 2),
        ('.limitted[1].composite.x', 'i16', 2),
        ('.limitted[1].composite.y', 'u8', 1),
        ('.limitted[1].composite.y.:final_padding', '<Pd1>', 1),
        ('.c_len (sizer)', 'u8', 1),
        ('.bound_scalar.:pre_padding', '<Pd7>', 7),
        ('.bound_scalar[@c_len]', 'i64', 8),
        ('.fixed_scalar[0]', 'i16', 2),
        ('.fixed_scalar[1]', 'i16', 2),
        ('.nested.:pre_padding', '<Pd4>', 4),
        ('.nested.m.structure.x', 'i16', 2),
        ('.nested.m.structure.y', 'u8', 1),
        ('.nested.m.structure.y.:final_padding', '<Pd1>', 1),
        ('.nested.m.scalar.:pre_padding', '<Pd4>', 4),
        ('.nested.m.scalar', 'i64', 8),
        ('.nested.n.x', 'i16', 2),
        ('.nested.n.y', 'u8', 1),
        ('.nested.n.y.:final_padding', '<Pd1>', 1),
        ('.nested.o', 'u32', 4),
        ('.b', '_bytes', 0),
    ]
