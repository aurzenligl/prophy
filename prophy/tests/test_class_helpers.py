import prophy


def get_helper_classes():
    class SubStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [
            ("a", prophy.array(prophy.u8, size=2)),
        ]

    class OneStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [
            ("x", prophy.u8),
            ("y", prophy.u32),
            ("o", prophy.optional(prophy.u32)),
        ]

    class SameStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [
            ("x", prophy.u8),
            ("y", prophy.u32),
            ("o", prophy.optional(prophy.u32)),
        ]

    class DifferentStruct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [
            ("x", prophy.u8),
            ("y", prophy.array(prophy.u32, size=1)),
            ("o", prophy.optional(prophy.u32)),
        ]

    class OneEnum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [
            ("x", 1),
            ("y", 2),
        ]

    class SameEnum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [
            ("x", 1),
            ("y", 2),
        ]

    class DifferentEnum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [
            ("x", 1),
            ("y", 3),
        ]

    class OneUnion(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [
            ("x", prophy.u8, 1),
            ("s", OneStruct, 2),
        ]

    class SameUnion(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [
            ("x", prophy.u8, 1),
            ("s", OneStruct, 2),
        ]

    class DifferentUnion(prophy.with_metaclass(prophy.union_generator, prophy.union)):
        _descriptor = [
            ("x", prophy.u8, 1),
            ("s", OneStruct, 3),
        ]
    return SubStruct, OneStruct, SameStruct, DifferentStruct, OneEnum, SameEnum, DifferentEnum, OneUnion, SameUnion, \
        DifferentUnion


def test_prophy_structs_equality():
    SubStruct, OneStruct, SameStruct, DifferentStruct, OneEnum, SameEnum, DifferentEnum, OneUnion, SameUnion, \
        DifferentUnion = get_helper_classes()

    check_eq(
        OneStruct, SameStruct, DifferentStruct, OneEnum, OneUnion, float, object
    )
    check_eq(
        OneEnum, SameEnum, DifferentEnum, OneStruct, OneUnion, float, object
    )
    check_eq(
        OneUnion, SameUnion, DifferentUnion, OneStruct, OneEnum, float, object
    )


def check_eq(one, same, *different_ones):
    assert one == same
    assert not one != same
    assert same == one
    assert not same != one

    for different in different_ones:
        assert one != different
        assert not one == different
        assert different != one
        assert not different == one
