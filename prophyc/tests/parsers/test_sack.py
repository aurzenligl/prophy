import os
import pytest

from prophyc import model

def parse(content, name = 'test.hpp', warn = None):
    from prophyc.parsers.sack import SackParser
    return SackParser(warn = warn).parse(content, name, None)

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
    assert parse(hpp) == [
        model.Struct("X", [
            model.StructMember("a", "u32"),
            model.StructMember("b", "u32"),
            model.StructMember("c", "u32")
        ])
    ]

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
    assert parse(hpp) == [
        model.Struct("X", [
            model.StructMember("a", "u8"),
            model.StructMember("b", "u16"),
            model.StructMember("c", "u32"),
            model.StructMember("d", "u64"),
            model.StructMember("e", "i8"),
            model.StructMember("f", "i16"),
            model.StructMember("g", "i32"),
            model.StructMember("h", "i64"),
            model.StructMember("i", "u8"),
            model.StructMember("j", "i8"),
            model.StructMember("k", "i8"),
            model.StructMember("n", "u32"),
            model.StructMember("o", "r32"),
            model.StructMember("p", "r64"),
            model.StructMember("r", "u32")
        ])
    ]

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
    assert parse(hpp) == [model.Struct("X", [model.StructMember("a", "i32")])]

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
    assert parse(hpp) == [
        model.Struct("OldStruct", [model.StructMember("a", "u32")]),
        model.Struct("X", [model.StructMember("a", "OldStruct")])
    ]

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
    assert parse(hpp) == [
        model.Struct("m__n__Namespaced", [model.StructMember("a", "u32")]),
        model.Struct("X", [model.StructMember("a", "m__n__Namespaced")])
    ]

@pytest.clang_installed
def test_array():
    hpp = """\
#include <stdint.h>
struct X
{
    uint32_t a[4];
};
"""
    assert parse(hpp) == [model.Struct("X", [model.StructMember("a", "u32", size = 4)])]

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
    assert parse(hpp) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]

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
    assert parse(hpp) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]

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
    assert parse(hpp) == [
        model.Enum("m__n__Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "m__n__Enum")
        ])
    ]

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
    assert parse(hpp) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_MinusOne", "0xFFFFFFFF"),
            model.EnumMember("Enum_MinusTwo", "0xFFFFFFFE"),
            model.EnumMember("Enum_MinusThree", "0xFFFFFFFD")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]

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
    assert parse(hpp) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum"),
            model.StructMember("b", "Enum"),
            model.StructMember("c", "Enum")
        ])
    ]

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
    assert parse(hpp) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]

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
    assert parse(hpp) == [
        model.Union("Union", [
            model.UnionMember("a", "u8", "0"),
            model.UnionMember("b", "u16", "1"),
            model.UnionMember("c", "u32", "2")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Union")
        ])
    ]

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
    assert parse(hpp) == [
        model.Union("Union", [
            model.UnionMember("a", "u8", "0")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Union")
        ])
    ]

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
    assert parse(hpp) == [
        model.Struct("X", [
            model.StructMember("a", "u8")
        ]),
        model.Struct("Y", [
            model.StructMember("a", "X")
        ]),
        model.Struct("Z", [
            model.StructMember("a", "X"),
            model.StructMember("b", "Y")
        ])
    ]

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

    """ I have no idea how to access class template members [A::a in example],
        having cursor to structure field typed as template class (instantiation) [X::a in example].
        Since parsing template class in context of data interchange protocol needs
        workaround anyway and - in longer run - removal, I'll leave a stub implementation which
        returns no members """

    assert parse(hpp) == [
        model.Struct("A__int__3__", []),
        model.Struct("X", [
            model.StructMember("a", "A__int__3__")
        ])
    ]

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
    assert parse(hpp) == [model.Struct("X", [model.StructMember("x", "i32")])]

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
    Anonymous = contains_cmp("X__anonymous__struct__at__")
    assert parse(hpp) == [
        model.Struct(Anonymous, [
            model.StructMember("b", "i8")
        ]),
        model.Struct("X", [
            model.StructMember("a", Anonymous, size = 3)
        ])
    ]

@pytest.clang_installed
def test_struct_with_incomplete_array():
    hpp = """\
struct X
{
    char b[];
};
"""
    assert parse(hpp) == [model.Struct('X', [model.StructMember('b', 'i8')])]

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
    nodes = parse(hpp, name = 'test-hyphen.hpp')

    assert '__hyphen__hpp__' in nodes[0].name

@pytest.clang_installed
def test_forward_declared_struct():
    hpp = """\
struct X;
"""
    assert parse(hpp) == []

@pytest.clang_installed
def test_omit_bitfields():
    hpp = """\
struct X
{
    unsigned a: 1;
    unsigned b: 1;
    unsigned c: 1;
    unsigned  : 5;
};
"""
    assert parse(hpp) == [model.Struct('X', [])]

class WarnMock(object):
    def __init__(self):
        self.warnings = []
    def __call__(self, msg, location = 'prophyc'):
        self.warnings.append((location, msg))

@pytest.clang_installed
def test_diagnostics_error():
    content = """\
unknown;
"""
    warn = WarnMock()

    assert parse(content,
        name = "x.cpp",
        warn = warn
    ) == []
    assert warn.warnings == [('x.cpp:1:1', 'C++ requires a type specifier for all declarations')]

@pytest.clang_installed
def test_diagnostics_warning():
    content = """\
int foo()
{
    int x;
}
"""
    warn = WarnMock()

    assert parse(content,
        name = "x.cpp",
        warn = warn
    ) == []
    assert warn.warnings == [('x.cpp:4:1', 'control reaches end of non-void function')]

@pytest.clang_installed
def test_libclang_parsing_error():
    with pytest.raises(model.ParseError) as e:
        parse('content', name = 'x')
    assert e.value.errors == [('x', 'error parsing translation unit')]
