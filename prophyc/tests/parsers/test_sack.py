import os
import tempfile

import pytest

def parse(content, suffix = '.hpp'):
    from prophyc.parsers.sack import SackParser
    try:
        with tempfile.NamedTemporaryFile(suffix = suffix, delete = False) as temp:
            temp.write(content)
            temp.flush()
            return SackParser().parse(temp.name)
    finally:
        os.unlink(temp.name)

class contains_cmp(object):
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return any((self.x in other, other in self.x))

@pytest.clang_installed
def test_simple_struct():
    hpp = """\
#include <stdint.h>
struct X
{
    uint32_t a;
    uint32_t b;
    uint32_t c;
};
"""
    nodes = parse(hpp)

    assert [("X", [("a", "u32", None, None, None, None),
                   ("b", "u32", None, None, None, None),
                   ("c", "u32", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_ints():
    hpp = """\
#include <stdint.h>
struct X
{
    uint8_t a;
    uint16_t b;
    uint32_t c;
    uint64_t d;
    int8_t e;
    int16_t f;
    int32_t g;
    int64_t h;
    unsigned char i;
    char j;
    signed char k;
    void* n;
    float o;
    double p;
    bool r;
};
"""
    nodes = parse(hpp)

    assert [("X", [("a", "u8", None, None, None, None),
                   ("b", "u16", None, None, None, None),
                   ("c", "u32", None, None, None, None),
                   ("d", "u64", None, None, None, None),
                   ("e", "i8", None, None, None, None),
                   ("f", "i16", None, None, None, None),
                   ("g", "i32", None, None, None, None),
                   ("h", "i64", None, None, None, None),
                   ("i", "u8", None, None, None, None),
                   ("j", "i8", None, None, None, None),
                   ("k", "i8", None, None, None, None),
                   ("n", "u32", None, None, None, None),
                   ("o", "r32", None, None, None, None),
                   ("p", "r64", None, None, None, None),
                   ("r", "u32", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_nested_typedefs():
    hpp = """\
typedef int my_int;
typedef my_int i_like_typedefs;
typedef i_like_typedefs i_really_do;
struct X
{
    i_really_do a;
};
"""
    nodes = parse(hpp)

    assert [("X", [("a", "i32", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_typedefed_struct():
    hpp = """\
#include <stdint.h>
typedef struct
{
    uint32_t a;
} OldStruct;
struct X
{
    OldStruct a;
};
"""
    nodes = parse(hpp)

    assert [("OldStruct", [("a", "u32", None, None, None, None)]),
            ("X", [("a", "OldStruct", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_namespaced_struct():
    hpp = """\
#include <stdint.h>
namespace m
{
namespace n
{
struct Namespaced
{
    uint32_t a;
};
}
}
struct X
{
    m::n::Namespaced a;
};
"""
    nodes = parse(hpp)

    assert [("m__n__Namespaced", [("a", "u32", None, None, None, None)]),
            ("X", [("a", "m__n__Namespaced", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_array():
    hpp = """\
#include <stdint.h>
struct X
{
    uint32_t a[4];
};
"""
    nodes = parse(hpp)

    assert [("X", [("a", "u32", True, None, 4, None)])] == nodes

@pytest.clang_installed
def test_enum():
    hpp = """\
enum Enum
{
    Enum_One = 1,
    Enum_Two = 2,
    Enum_Three = 3
};
struct X
{
    Enum a;
};
"""
    nodes = parse(hpp)

    assert [("Enum", [("Enum_One", "1"),
                      ("Enum_Two", "2"),
                      ("Enum_Three", "3")]),
            ("X", [("a", "Enum", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_typedefed_enum():
    hpp = """\
typedef enum Enum
{
    Enum_One = 1,
    Enum_Two = 2,
    Enum_Three = 3
} Enum;
struct X
{
    Enum a;
};
"""
    nodes = parse(hpp)

    assert [("Enum", [("Enum_One", "1"),
                      ("Enum_Two", "2"),
                      ("Enum_Three", "3")]),
            ("X", [("a", "Enum", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_namespaced_enum():
    hpp = """\
namespace m
{
namespace n
{
enum Enum
{
    Enum_One = 1,
    Enum_Two = 2,
    Enum_Three = 3
};
}
}
struct X
{
    m::n::Enum a;
};
"""
    nodes = parse(hpp)

    assert [("m__n__Enum", [("Enum_One", "1"),
                            ("Enum_Two", "2"),
                            ("Enum_Three", "3")]),
            ("X", [("a", "m__n__Enum", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_enum_with_negative_one_values():
    hpp = """\
enum Enum
{
    Enum_MinusOne = -1,
    Enum_MinusTwo = -2,
    Enum_MinusThree = -3
};
struct X
{
    Enum a;
};
"""
    nodes = parse(hpp)

    assert [("Enum", [("Enum_MinusOne", "0xFFFFFFFF"),
                      ("Enum_MinusTwo", "0xFFFFFFFE"),
                      ("Enum_MinusThree", "0xFFFFFFFD")]),
            ("X", [("a", "Enum", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_multiple_enums():
    hpp = """\
typedef enum Enum
{
    Enum_One = 1,
    Enum_Two = 2,
    Enum_Three = 3
} Enum;
struct X
{
    Enum a;
    Enum b;
    Enum c;
};
"""
    nodes = parse(hpp)

    assert [("Enum", [("Enum_One", "1"),
                      ("Enum_Two", "2"),
                      ("Enum_Three", "3")]),
            ("X", [("a", "Enum", None, None, None, None),
                   ("b", "Enum", None, None, None, None),
                   ("c", "Enum", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_c_enum():
    hpp = """\
typedef enum
{
    Enum_One = 1,
    Enum_Two = 2,
    Enum_Three = 3
} Enum;
struct X
{
    Enum a;
};
"""
    nodes = parse(hpp)

    assert [("Enum", [("Enum_One", "1"),
                      ("Enum_Two", "2"),
                      ("Enum_Three", "3")]),
            ("X", [("a", "Enum", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_union():
    hpp = """\
#include <stdint.h>
union Union
{
    uint8_t a;
    uint16_t b;
    uint32_t c;
};
struct X
{
    Union a;
};
"""
    nodes = parse(hpp)

    assert [("Union", [("a", "u8", "0"),
                       ("b", "u16", "1"),
                       ("c", "u32", "2")]),
            ("X", [("a", "Union", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_typedefed_union():
    hpp = """\
#include <stdint.h>
typedef union
{
    uint8_t a;
} Union;
struct X
{
    Union a;
};
"""
    nodes = parse(hpp)

    assert [("Union", [("a", "u8", "0")]),
            ("X", [("a", "Union", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_multiple_structs():
    hpp = """\
#include <stdint.h>
struct X
{
    uint8_t a;
};
struct Y
{
    X a;
};
struct Z
{
    X a;
    Y b;
};
"""
    nodes = parse(hpp)

    assert [("X", [("a", "u8", None, None, None, None)]),
            ("Y", [("a", "X", None, None, None, None)]),
            ("Z", [("a", "X", None, None, None, None),
                   ("b", "Y", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_class_template():
    hpp = """\
#include <stdint.h>
#include <stddef.h>
template<typename T, size_t N>
class A
{
    T a[N];
};
struct X
{
    A<int, 3> a;
};
"""
    nodes = parse(hpp)

    """ I have no idea how to access class template members [A::a in example],
        having cursor to structure field typed as template class (instantiation) [X::a in example].
        Since parsing template class in context of data interchange protocol needs
        workaround anyway and - in longer run - removal, I'll leave a stub implementation which
        returns no members """

    assert [("A__int__3__", []),
            ("X", [("a", "A__int__3__", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_c_struct():
    hpp = """\
#ifdef __cplusplus
extern "C" {
#endif
struct X
{
    int x;
};
typedef struct X X;
#ifdef __cplusplus
}
#endif
"""
    nodes = parse(hpp)

    assert [("X", [("x", "i32", None, None, None, None)])] == nodes

@pytest.clang_installed
def test_struct_with_anonymous_struct():
    hpp = """\
struct X
{
    struct
    {
        char b;
    } a[3];
};
"""
    nodes = parse(hpp)

    Anonymous = contains_cmp("X__anonymous__struct__at__")

    assert [(Anonymous, [("b", "i8", None, None, None, None)]),
            ("X", [("a", Anonymous, True, None, 3, None)])] == nodes

@pytest.clang_installed
def test_struct_with_incomplete_array():
    hpp = """\
struct X
{
    char b[];
};
"""
    nodes = parse(hpp)

    assert [('X', [('b', 'i8', None, None, None, None)])] == nodes

@pytest.clang_installed
def test_struct_with_incomplete_array_in_file_with_hyphen():
    hpp = """\
struct X
{
    struct
    {
        char a;
    } a;
};
"""
    nodes = parse(hpp, suffix = '-hyphen.hpp')

    assert '__hyphen__hpp__' in nodes[0].name

@pytest.clang_installed
def test_forward_declared_struct():
    hpp = """\
struct X;
"""
    nodes = parse(hpp)

    assert nodes == []

@pytest.clang_installed
def test_omit_bitfields():
    hpp = """\
typedef struct X
{
    unsigned a: 1;
    unsigned b: 1;
    unsigned c: 1;
    unsigned  : 5;
};
"""

    nodes = parse(hpp)

    assert nodes == [('X', [])]
