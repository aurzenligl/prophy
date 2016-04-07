from prophyc import model
from prophyc.generators.cpp import CppGenerator

def process(nodes):
    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    model.evaluate_sizes(nodes)
    return nodes

def generate_definitions(nodes):
    process(nodes)
    return CppGenerator().generate_definitions(nodes)

def generate_swap_declarations(nodes):
    process(nodes)
    return CppGenerator().generate_swap_declarations(nodes)

def generate_swap(nodes):
    process(nodes)
    return CppGenerator().generate_swap(nodes)

def generate_hpp(nodes, basename):
    process(nodes)
    return CppGenerator().serialize_string_hpp(nodes, basename)

def generate_cpp(nodes, basename):
    process(nodes)
    return CppGenerator().serialize_string_cpp(nodes, basename)

def test_definitions_includes():
    nodes = [model.Include("szydlo", []),
             model.Include("mydlo", []),
             model.Include("powidlo", [])]

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
    nodes = [model.Struct("Struct", [(model.StructMember("a", "u8")),
                                     (model.StructMember("b", "i64")),
                                     (model.StructMember("c", "r32")),
                                     (model.StructMember("d", "TTypeX"))])]

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
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems"),
                                     model.StructMember("a", "u8", bound = "tmpName")])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    TNumberOfItems tmpName;
    uint8_t a[1]; /// dynamic array, size in tmpName
};
"""

def test_definitions_struct_with_fixed_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", size = "NUM_OF_ARRAY_ELEMS")])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a[NUM_OF_ARRAY_ELEMS];
};
"""

def test_definitions_struct_with_limited_array():
    nodes = [model.Struct("Struct", [model.StructMember("a_len", "u8"),
                                     model.StructMember("a", "u8", bound = "a_len", size = "NUM_OF_ARRAY_ELEMS")])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a_len;
    uint8_t a[NUM_OF_ARRAY_ELEMS]; /// limited array, size in a_len
};
"""

def test_definitions_struct_with_ext_sized_array():
    nodes = [model.Struct("Struct", [model.StructMember("count", "u8"),
                                     model.StructMember("a", "u8", bound = "count"),
                                     model.StructMember("b", "u8", bound = "count"),
                                     model.StructMember("c", "u8", bound = "count")])]

    print generate_definitions(nodes)
    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t count;
    uint8_t a[1]; /// dynamic array, size in count

    struct part2
    {
        uint8_t b[1]; /// dynamic array, size in count
    } _2;

    struct part3
    {
        uint8_t c[1]; /// dynamic array, size in count
    } _3;
};
"""

def test_definitions_struct_with_byte():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte")])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a;
};
"""

def test_definitions_struct_with_byte_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", unlimited = True)])]

    assert generate_definitions(nodes) == """\
struct Struct
{
    uint8_t a[1]; /// greedy array
};
"""

def test_definitions_struct_many_arrays():
    nodes = [
        model.Struct("ManyArrays", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a"),
            model.StructMember("num_of_b", "u8"),
            model.StructMember("b", "u8", bound = "num_of_b"),
            model.StructMember("num_of_c", "u8"),
            model.StructMember("c", "u8", bound = "num_of_c")
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
            model.StructMember("num_of_a", "u8"),
            model.StructMember("num_of_b", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a"),
            model.StructMember("b", "u8", bound = "num_of_b")
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

def test_definitions_struct_many_arrays_bounded_by_the_same_member():
    nodes = [
        model.Struct("ManyArraysBoundedByTheSame", [
            model.StructMember("num_of_elements", "u8"),
            model.StructMember("dummy", "u8"),
            model.StructMember("a", "u8", bound = "num_of_elements"),
            model.StructMember("b", "u8", bound = "num_of_elements")
        ])
    ]

    assert generate_definitions(nodes) == """\
struct ManyArraysBoundedByTheSame
{
    uint8_t num_of_elements;
    uint8_t dummy;
    uint8_t a[1]; /// dynamic array, size in num_of_elements

    struct part2
    {
        uint8_t b[1]; /// dynamic array, size in num_of_elements
    } _2;
};
"""

def test_definitions_struct_with_dynamic_fields():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a")
        ]),
        model.Struct("X", [
            model.StructMember("a", "u8"),
            model.StructMember("b", "Dynamic"),
            model.StructMember("c", "u8")
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
            (model.StructMember("a", "u8", optional = True))
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
             model.Struct("A", [model.StructMember("a", "u32")]),
             model.Struct("B", [model.StructMember("b", "u32")])]

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

def test_swap_empty_struct():
    nodes = [
        model.Struct("X", [])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    return payload + 1;
}
"""

def test_swap_struct_with_fixed_element():
    nodes = [
        model.Struct("X", [
            (model.StructMember("a", "u8"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(&payload->a);
    return payload + 1;
}
"""

def test_swap_struct_with_optional_element():
    nodes = [
        model.Struct("X", [
            (model.StructMember("x", "u32", optional = True)),
            (model.StructMember("y", "Y", optional = True))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(&payload->has_x);
    if (payload->has_x) swap(&payload->x);
    swap(&payload->has_y);
    if (payload->has_y) swap(&payload->y);
    return payload + 1;
}
"""

def test_swap_union():
    nodes = [
        model.Union("X", [
            (model.UnionMember("a", "u8", 1)),
            (model.UnionMember("b", "u64", 2)),
            (model.UnionMember("c", "C", 3))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {
        case X::discriminator_a: swap(&payload->a); break;
        case X::discriminator_b: swap(&payload->b); break;
        case X::discriminator_c: swap(&payload->c); break;
        default: break;
    }
    return payload + 1;
}
"""

def test_swap_struct_with_fixed_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("x", "u16", size = 5))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap_n_fixed(payload->x, 5);
    return payload + 1;
}
"""

def test_swap_struct_with_limited_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u16")),
            (model.StructMember("x", "Y", bound = "num_of_x", size = 3))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}
"""

def test_swap_struct_with_dynamic_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("x", "u16", bound = "num_of_x"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    return cast<X*>(swap_n_fixed(payload->x, payload->num_of_x));
}
"""

def test_swap_struct_with_ext_sized_array_of_fixed_elements():
    nodes = [
        model.Struct("X", [
            (model.StructMember("szr", "u32")),
            (model.StructMember("x", "u16", bound = "szr")),
            (model.StructMember("y", "u16", bound = "szr"))
        ])
    ]

    assert generate_swap(nodes) == """\
inline X::part2* swap(X::part2* payload, size_t szr)
{
    return cast<X::part2*>(swap_n_fixed(payload->y, szr));
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->szr);
    X::part2* part2 = cast<X::part2*>(swap_n_fixed(payload->x, payload->szr));
    return cast<X*>(swap(part2, payload->szr));
}
"""

def test_swap_struct_with_greedy_array():
    nodes = [
        model.Struct("X", [
            (model.StructMember("x", "u8")),
            (model.StructMember("y", "Y", unlimited = True))
        ]),
        model.Struct("Z", [
            (model.StructMember("z", "X"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(&payload->x);
    return cast<X*>(payload->y);
}

template <>
Z* swap<Z>(Z* payload)
{
    return cast<Z*>(&payload->z);
}
"""

def test_swap_enum_in_struct():
    nodes = [
        model.Enum("E1", [
            model.EnumMember("E1_A", "0")
        ]),
        model.Struct("X", [
            (model.StructMember("x", "E1"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
X* swap<X>(X* payload)
{
    swap(&payload->x);
    return payload + 1;
}
"""

def test_swap_enum_in_arrays():
    nodes = [
        model.Enum("E1", [
            model.EnumMember("E1_A", "0")
        ]),
        model.Struct("EnumArrays", [
            (model.StructMember("a", "E1", size = 2)),
            (model.StructMember("num_of_b", "u32")),
            (model.StructMember("b", "E1", size = 2, bound = "num_of_b")),
            (model.StructMember("num_of_c", "u32")),
            (model.StructMember("c", "E1", bound = "num_of_c"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
EnumArrays* swap<EnumArrays>(EnumArrays* payload)
{
    swap_n_fixed(payload->a, 2);
    swap(&payload->num_of_b);
    swap_n_fixed(payload->b, payload->num_of_b);
    swap(&payload->num_of_c);
    return cast<EnumArrays*>(swap_n_fixed(payload->c, payload->num_of_c));
}
"""

def test_swap_enum_in_greedy_array():
    nodes = [
        model.Enum("E1", [
            model.EnumMember("E1_A", "0")
        ]),
        model.Struct("EnumGreedyArray", [
            (model.StructMember("x", "E1", unlimited = True))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
EnumGreedyArray* swap<EnumGreedyArray>(EnumGreedyArray* payload)
{
    return cast<EnumGreedyArray*>(payload->x);
}
"""

def test_swap_enum_in_union():
    nodes = [
        model.Enum("E1", [
            model.EnumMember("E1_A", "0")
        ]),
        model.Union("EnumUnion", [
            (model.UnionMember("x", "E1", 1)),
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
EnumUnion* swap<EnumUnion>(EnumUnion* payload)
{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {
        case EnumUnion::discriminator_x: swap(&payload->x); break;
        default: break;
    }
    return payload + 1;
}
"""

def test_swap_struct_with_dynamic_element():
    nodes = [
        model.Struct("Dynamic", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("x", "u16", bound = "num_of_x"))
        ]),
        model.Struct("X", [
            (model.StructMember("a", "Dynamic"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
Dynamic* swap<Dynamic>(Dynamic* payload)
{
    swap(&payload->num_of_x);
    return cast<Dynamic*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
X* swap<X>(X* payload)
{
    return cast<X*>(swap(&payload->a));
}
"""

def test_swap_struct_with_dynamic_array_of_dynamic_elements():
    nodes = [
        model.Struct("Y", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("x", "u16", bound = "num_of_x"))
        ]),
        model.Struct("X", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("x", "Y", bound = "num_of_x"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
Y* swap<Y>(Y* payload)
{
    swap(&payload->num_of_x);
    return cast<Y*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    return cast<X*>(swap_n_dynamic(payload->x, payload->num_of_x));
}
"""

def test_swap_struct_with_many_arrays():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("x", "u32", bound = "num_of_x")),
            (model.StructMember("num_of_y", "u32")),
            (model.StructMember("y", "u32", bound = "num_of_y")),
            (model.StructMember("num_of_z", "u32")),
            (model.StructMember("z", "u32", bound = "num_of_z"))
        ])
    ]

    assert generate_swap(nodes) == """\
inline X::part2* swap(X::part2* payload)
{
    swap(&payload->num_of_y);
    return cast<X::part2*>(swap_n_fixed(payload->y, payload->num_of_y));
}

inline X::part3* swap(X::part3* payload)
{
    swap(&payload->num_of_z);
    return cast<X::part3*>(swap_n_fixed(payload->z, payload->num_of_z));
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    X::part2* part2 = cast<X::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    X::part3* part3 = cast<X::part3*>(swap(part2));
    return cast<X*>(swap(part3));
}
"""

def test_swap_struct_with_many_arrays_bounded_by_the_same_member():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_elements", "u32")),
            (model.StructMember("dummy", "u32")),
            (model.StructMember("x", "u32", bound = "num_of_elements")),
            (model.StructMember("y", "u32", bound = "num_of_elements"))
        ])
    ]

    assert generate_swap(nodes) == """\
inline X::part2* swap(X::part2* payload, size_t num_of_elements)
{
    return cast<X::part2*>(swap_n_fixed(payload->y, num_of_elements));
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_elements);
    swap(&payload->dummy);
    X::part2* part2 = cast<X::part2*>(swap_n_fixed(payload->x, payload->num_of_elements));
    return cast<X*>(swap(part2, payload->num_of_elements));
}
"""

def test_swap_struct_with_many_arrays_passing_numbering_fields():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("num_of_y", "u32")),
            (model.StructMember("x", "u32", bound = "num_of_x")),
            (model.StructMember("y", "u32", bound = "num_of_y"))
        ])
    ]

    assert generate_swap(nodes) == """\
inline X::part2* swap(X::part2* payload, size_t num_of_y)
{
    return cast<X::part2*>(swap_n_fixed(payload->y, num_of_y));
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    swap(&payload->num_of_y);
    X::part2* part2 = cast<X::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<X*>(swap(part2, payload->num_of_y));
}
"""

def test_swap_struct_with_many_arrays_passing_numbering_fields_heavily():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_a", "u32")),
            (model.StructMember("num_of_b", "u32")),
            (model.StructMember("b", "u16", bound = "num_of_b")),
            (model.StructMember("num_of_c", "u32")),
            (model.StructMember("c", "u16", bound = "num_of_c")),
            (model.StructMember("a", "u16", bound = "num_of_a"))
        ])
    ]

    assert generate_swap(nodes) == """\
inline X::part2* swap(X::part2* payload)
{
    swap(&payload->num_of_c);
    return cast<X::part2*>(swap_n_fixed(payload->c, payload->num_of_c));
}

inline X::part3* swap(X::part3* payload, size_t num_of_a)
{
    return cast<X::part3*>(swap_n_fixed(payload->a, num_of_a));
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_a);
    swap(&payload->num_of_b);
    X::part2* part2 = cast<X::part2*>(swap_n_fixed(payload->b, payload->num_of_b));
    X::part3* part3 = cast<X::part3*>(swap(part2));
    return cast<X*>(swap(part3, payload->num_of_a));
}
"""

def test_swap_struct_with_dynamic_field_and_tail_fixed():
    nodes = [
        model.Struct("X", [
            (model.StructMember("num_of_x", "u8")),
            (model.StructMember("x", "u8", bound = "num_of_x")),
            (model.StructMember("y", "u32")),
            (model.StructMember("z", "u64"))
        ])
    ]

    assert generate_swap(nodes) == """\
inline X::part2* swap(X::part2* payload)
{
    swap(&payload->y);
    swap(&payload->z);
    return payload + 1;
}

template <>
X* swap<X>(X* payload)
{
    swap(&payload->num_of_x);
    X::part2* part2 = cast<X::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<X*>(swap(part2));
}
"""

def test_swap_struct_with_many_dynamic_fields():
    nodes = [
        model.Struct("Y", [
            (model.StructMember("num_of_x", "u32")),
            (model.StructMember("x", "u16", bound = "num_of_x"))
        ]),
        model.Struct("X", [
            (model.StructMember("x", "Y")),
            (model.StructMember("y", "Y")),
            (model.StructMember("z", "Y"))
        ])
    ]

    assert generate_swap(nodes) == """\
template <>
Y* swap<Y>(Y* payload)
{
    swap(&payload->num_of_x);
    return cast<Y*>(swap_n_fixed(payload->x, payload->num_of_x));
}

inline X::part2* swap(X::part2* payload)
{
    return cast<X::part2*>(swap(&payload->y));
}

inline X::part3* swap(X::part3* payload)
{
    return cast<X::part3*>(swap(&payload->z));
}

template <>
X* swap<X>(X* payload)
{
    X::part2* part2 = cast<X::part2*>(swap(&payload->x));
    X::part3* part3 = cast<X::part3*>(swap(part2));
    return cast<X*>(swap(part3));
}
"""

def test_generate_swap_declarations():
    nodes = [
        model.Struct("A", [
            (model.StructMember("x", "u32")),
        ]),
        model.Union("B", [
            (model.UnionMember("x", "u32", 1)),
        ]),
        model.Enum("C", [
            model.EnumMember("E1_A", "0")
        ])
    ]

    assert generate_swap_declarations(nodes) == """\
namespace prophy
{

template <> inline C* swap<C>(C* in) { swap(reinterpret_cast<uint32_t*>(in)); return in + 1; }
template <> A* swap<A>(A*);
template <> B* swap<B>(B*);

} // namespace prophy
"""

def test_generate_empty_file():
    assert generate_hpp([], "TestEmpty") == """\
#ifndef _PROPHY_GENERATED_TestEmpty_HPP
#define _PROPHY_GENERATED_TestEmpty_HPP

#include <prophy/prophy.hpp>


namespace prophy
{


} // namespace prophy

#endif  /* _PROPHY_GENERATED_TestEmpty_HPP */
"""

    assert generate_cpp([], "TestEmpty") == """\
#include <prophy/detail/prophy.hpp>

#include \"TestEmpty.pp.hpp\"

using namespace prophy::detail;

namespace prophy
{


} // namespace prophy
"""

def test_generate_file():
    nodes = [
        model.Struct("Struct", [
            (model.StructMember("a", "u8"))
        ])
    ]

    assert generate_hpp(nodes, "TestFile") == """\
#ifndef _PROPHY_GENERATED_TestFile_HPP
#define _PROPHY_GENERATED_TestFile_HPP

#include <prophy/prophy.hpp>

struct Struct
{
    uint8_t a;
};

namespace prophy
{

template <> Struct* swap<Struct>(Struct*);

} // namespace prophy

#endif  /* _PROPHY_GENERATED_TestFile_HPP */
"""

    assert generate_cpp(nodes, "TestFile") == """\
#include <prophy/detail/prophy.hpp>

#include "TestFile.pp.hpp"

using namespace prophy::detail;

namespace prophy
{

template <>
Struct* swap<Struct>(Struct* payload)
{
    swap(&payload->a);
    return payload + 1;
}

} // namespace prophy
"""
