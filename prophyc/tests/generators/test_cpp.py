from prophyc import model
from prophyc.generators.cpp import CppGenerator

def generate_definitions(nodes):
    return CppGenerator().generate_definitions(nodes)

def generate_swap(nodes):
    return CppGenerator().generate_swap(nodes)

def generate_file(nodes, basename):
    return CppGenerator().serialize_string(nodes, basename)

def test_definitions_includes():
    nodes = [model.Include("szydlo"),
             model.Include("mydlo"),
             model.Include("powidlo")]

    assert generate_definitions(nodes) == """\
#include "szydlo.pp.hpp"
#include "mydlo.pp.hpp"
#include "powidlo.pp.hpp"
"""

def test_definitions_constants():
    nodes = [model.Constant("CONST_A", "0"),
             model.Constant("CONST_B", "31")]

    assert generate_definitions(nodes) == """\
enum { CONST_A = 0 };
enum { CONST_B = 31 };
"""

def test_definitions_typedefs():
    nodes = [model.Typedef("a", "b"),
             model.Typedef("c", "u8"),]

    assert generate_definitions(nodes) == """\
typedef b a;
typedef uint8_t c;
"""

def test_definitions_enums():
    nodes = [model.Enum("EEnum", [model.EnumMember("EEnum_A", "0"),
                                  model.EnumMember("EEnum_B", "1"),
                                  model.EnumMember("EEnum_C", "2")])]

    assert generate_definitions(nodes) == """\
enum EEnum
{
    EEnum_A = 0,
    EEnum_B = 1,
    EEnum_C = 2
};
"""

def test_definitions_struct():
    nodes = [model.Struct("Struct", [(model.StructMember("a", "u8", None, None, None, False)),
                                     (model.StructMember("b", "i64", None, None, None, False)),
                                     (model.StructMember("c", "r32", None, None, None, False)),
                                     (model.StructMember("d", "TTypeX", None, None, None, False))])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a;
    int64_t b;
    float c;
    TTypeX d;
};
"""

def test_definitions_struct_with_dynamic_array():
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems", None, None, None, False),
                                     model.StructMember("a", "u8", True, "tmpName", None, False)])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    TNumberOfItems tmpName;
    uint8_t a[1]; /// dynamic array, size in tmpName
};
"""

def test_definitions_struct_with_fixed_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", True, None, "NUM_OF_ARRAY_ELEMS", False)])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a[NUM_OF_ARRAY_ELEMS];
};
"""

def test_definitions_struct_with_limited_array():
    nodes = [model.Struct("Struct", [model.StructMember("a_len", "u8", None, None, None, False),
                                     model.StructMember("a", "u8", True, "a_len", "NUM_OF_ARRAY_ELEMS", False)])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a_len;
    uint8_t a[NUM_OF_ARRAY_ELEMS]; /// limited array, size in a_len
};
"""

def test_definitions_struct_with_byte():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", False, None, None, None)])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a;
};
"""

def test_definitions_struct_with_byte_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", True, None, None, None)])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a[1]; /// greedy array
};
"""

def test_definitions_struct_many_arrays():
    nodes = [
        model.Struct("ManyArrays", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False),
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False),
            model.StructMember("num_of_c", "u8", None, None, None, False),
            model.StructMember("c", "u8", True, "num_of_c", None, False)
        ])
    ]

    assert generate_definitions(nodes) == """\
struct ManyArrays
{
    uint8_t num_of_a;
    uint8_t a[1]; /// dynamic array, size in num_of_a

    struct part2
    {
        uint8_t num_of_b;
        uint8_t b[1]; /// dynamic array, size in num_of_b
    } _2;

    struct part3
    {
        uint8_t num_of_c;
        uint8_t c[1]; /// dynamic array, size in num_of_c
    } _3;
};
"""

def test_definitions_struct_many_arrays_mixed():
    nodes = [
        model.Struct("ManyArraysMixed", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False)
        ])
    ]

    assert generate_definitions(nodes) == """\
struct ManyArraysMixed
{
    uint8_t num_of_a;
    uint8_t num_of_b;
    uint8_t a[1]; /// dynamic array, size in num_of_a

    struct part2
    {
        uint8_t b[1]; /// dynamic array, size in num_of_b
    } _2;
};
"""

def test_definitions_struct_with_dynamic_fields():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False)
        ]),
        model.Struct("X", [
            model.StructMember("a", "u8", None, None, None, False),
            model.StructMember("b", "Dynamic", None, None, None, False),
            model.StructMember("c", "u8", None, None, None, False)
        ])
    ]

    assert generate_definitions(nodes) == """\
struct Dynamic
{
    uint8_t num_of_a;
    uint8_t a[1]; /// dynamic array, size in num_of_a
};

struct X
{
    uint8_t a;
    Dynamic b;

    struct part2
    {
        uint8_t c;
    } _2;
};
"""

def test_definitions_struct_with_optional_field():
    nodes = [
        model.Struct("Struct", [
            (model.StructMember("a", "u8", None, None, None, True))
        ])
    ]

    assert generate_definitions(nodes) == """\
struct Struct
{
    prophy::bool_t has_a;
    uint8_t a;
};
"""

def test_definitions_union():
    nodes = [
        model.Union("Union", [
            (model.UnionMember("a", "u8", 1)),
            (model.UnionMember("b", "u64", 2)),
            (model.UnionMember("c", "Composite", 3))
        ])
    ]

    assert generate_definitions(nodes) == """\
struct Union
{
    enum _discriminator
    {
        discriminator_a = 1,
        discriminator_b = 2,
        discriminator_c = 3
    } discriminator;

    union
    {
        uint8_t a;
        uint64_t b;
        Composite c;
    };
};
"""

def test_definitions_newlines():
    nodes = [model.Typedef("a", "b"),
             model.Typedef("c", "d"),
             model.Enum("E1", [model.EnumMember("E1_A", "0")]),
             model.Enum("E2", [model.EnumMember("E2_A", "0")]),
             model.Constant("CONST_A", "0"),
             model.Typedef("e", "f"),
             model.Constant("CONST_B", "0"),
             model.Constant("CONST_C", "0"),
             model.Struct("A", [model.StructMember("a", "u32", False, None, None, None)]),
             model.Struct("B", [model.StructMember("b", "u32", False, None, None, None)])]

    assert generate_definitions(nodes) == """\
typedef b a;
typedef d c;

enum E1
{
    E1_A = 0
};

enum E2
{
    E2_A = 0
};

enum { CONST_A = 0 };

typedef f e;

enum { CONST_B = 0 };
enum { CONST_C = 0 };

struct A
{
    uint32_t a;
};

struct B
{
    uint32_t b;
};
"""

def test_swap_struct_with_fixed_element():
    nodes = [
        model.Struct("X", [
            (model.StructMember("a", "u8", None, None, None, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline X* swap<X>(X* payload)
{
    swap(&payload->a);
    return payload + 1;
}
"""

def test_swap_struct_with_enum_element():
    pass

def test_swap_struct_with_optional_element():
    pass

def test_swap_struct_with_fixed_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("x", "u16", True, None, 5, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline X* swap<X>(X* payload)
{
    swap_n_fixed(payload->x, 5);
    return payload + 1;
}
"""

def test_swap_struct_with_limited_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u16", False, None, None, False)),
            (model.StructMember("x", "Y", True, "num_of_x", 3, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}
"""

def test_swap_struct_with_dynamic_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u32", None, None, None, False)),
            (model.StructMember("x", "u16", True, "num_of_x", None, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    return cast<X*>(swap_n_fixed(payload->x, payload->num_of_x));
}
"""

def test_swap_struct_with_greedy_array():
    nodes = [
        model.Struct("X", [
            (model.StructMember("x", "u8", None, None, None, False)),
            (model.StructMember("y", "Y", True, None, None, False))
        ]),
        model.Struct("Z", [
            (model.StructMember("z", "X", None, None, None, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline X* swap<X>(X* payload)
{
    swap(&payload->x);
    return cast<X*>(payload->y);
}

template <>
inline Z* swap<Z>(Z* payload)
{
    return cast<Z*>(&payload->z);
}
"""

def test_swap_struct_with_dynamic_element():
    nodes = [
        model.Struct("Dynamic", [
            (model.StructMember("num_of_x", "u32", None, None, None, False)),
            (model.StructMember("x", "u16", True, "num_of_x", None, False))
        ]),
        model.Struct("X", [
            (model.StructMember("a", "Dynamic", None, None, None, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline Dynamic* swap<Dynamic>(Dynamic* payload)
{
    swap(&payload->num_of_x);
    return cast<Dynamic*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
inline X* swap<X>(X* payload)
{
    return cast<X*>(swap(&payload->a));
}
"""

def test_swap_struct_with_dynamic_array_of_dynamic_elements():
    nodes = [
        model.Struct("Y", [
            (model.StructMember("num_of_x", "u32", None, None, None, False)),
            (model.StructMember("x", "u16", True, "num_of_x", None, False))
        ]),
        model.Struct("X", [
            (model.StructMember("num_of_x", "u32", None, None, None, False)),
            (model.StructMember("x", "Y", True, "num_of_x", None, False))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
inline Y* swap<Y>(Y* payload)
{
    swap(&payload->num_of_x);
    return cast<Y*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
inline X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    return cast<X*>(swap_n_dynamic(payload->x, payload->num_of_x));
}
"""

def test_swap_struct_with_many_arrays():
    pass

def test_swap_struct_with_many_arrays_passing_numbering_fields():
    pass

def test_swap_struct_with_many_dynamic_fields():
    pass

def test_swap_union():
    pass

def test_generate_file():
    nodes = [
        model.Struct("Struct", [
            (model.StructMember("a", "u8", None, None, None, False))
        ])
    ]

    assert generate_file(nodes, "TestFile") == """\
#ifndef _PROPHY_GENERATED_TestFile_HPP
#define _PROPHY_GENERATED_TestFile_HPP

#include <prophy/prophy.hpp>

struct Struct
{
    uint8_t a;
};

#endif  /* _PROPHY_GENERATED_TestFile_HPP */
"""
