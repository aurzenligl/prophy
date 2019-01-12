import pytest

from prophyc import model


def parse(content, extension='.hpp', warn=None, includes=[]):
    from prophyc.parsers.sack import SackParser
    file_name = 'test'
    return SackParser(warn=warn, include_dirs=includes).parse(content, file_name + extension, None)


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_simple_struct(if_clang_installed, extension):
    hpp = """\
#include <stdint.h>
struct X
{
    uint32_t a;
    uint32_t b;
    uint32_t c;
};
"""
    assert parse(hpp, extension) == [
        model.Struct("X", [
            model.StructMember("a", "u32"),
            model.StructMember("b", "u32"),
            model.StructMember("c", "u32")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_ints(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
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
            model.StructMember("r", "i32")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_nested_typedefs(if_clang_installed, extension):
    hpp = """\
typedef int my_int;
typedef my_int i_like_typedefs;
typedef i_like_typedefs i_really_do;
struct X
{
    i_really_do a;
};
"""
    assert parse(hpp, extension) == [model.Struct("X", [model.StructMember("a", "i32")])]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_typedefed_struct(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Struct("OldStruct", [model.StructMember("a", "u32")]),
        model.Struct("X", [model.StructMember("a", "OldStruct")])
    ]


def test_namespaced_struct(if_clang_installed, ):
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


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_array(if_clang_installed, extension):
    hpp = """\
#include <stdint.h>
struct X
{
    uint32_t a[4];
};
"""
    assert parse(hpp, extension) == [
        model.Struct("X", [
            model.StructMember("a", "u32", size=4)
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_enum(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_typedefed_enum(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]


def test_namespaced_enum(if_clang_installed, ):
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


def test_namespaced_typedef(if_clang_installed, ):
    hpp = """\
#include <stdint.h>
namespace N { typedef uint32_t u32; }
struct X
{
    N::u32 x;
};
"""
    assert parse(hpp) == [
        model.Struct('X', [
            model.StructMember('x', 'u32')
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_enum_with_negative_one_values(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_MinusOne", "0xFFFFFFFF"),
            model.EnumMember("Enum_MinusTwo", "0xFFFFFFFE"),
            model.EnumMember("Enum_MinusThree", "0xFFFFFFFD")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_multiple_enums(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
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


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_c_enum(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Enum("Enum", [
            model.EnumMember("Enum_One", "1"),
            model.EnumMember("Enum_Two", "2"),
            model.EnumMember("Enum_Three", "3")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Enum")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_union(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Union("Union", [
            model.UnionMember("a", "u8", "0"),
            model.UnionMember("b", "u16", "1"),
            model.UnionMember("c", "u32", "2")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Union")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_typedefed_union(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Union("Union", [
            model.UnionMember("a", "u8", "0")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Union")
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_multiple_structs(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
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


def test_class_template(if_clang_installed, ):
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


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_c_struct(if_clang_installed, extension):
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
    assert parse(hpp, extension) == [
        model.Struct("X", [
            model.StructMember("x", "i32")
        ])
    ]


def test_struct_with_anonymous_struct(if_clang_installed, ):
    hpp = """\
struct X
{
    struct
    {
        char b;
    } a[3];
};
"""
    assert parse(hpp, '.h') == [
        model.Struct("X__anonymous__at__test__h__3__5__", [
            model.StructMember("b", "i8")
        ]),
        model.Struct("X", [
            model.StructMember("a", "X__anonymous__at__test__h__3__5__", size=3)
        ])
    ]
    assert parse(hpp, '.hpp') == [
        model.Struct("X__anonymous__struct__at__test__hpp__3__5__", [
            model.StructMember("b", "i8")
        ]),
        model.Struct("X", [
            model.StructMember("a", "X__anonymous__struct__at__test__hpp__3__5__", size=3)
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_struct_with_incomplete_array(if_clang_installed, extension):
    hpp = """\
struct X
{
    char b[];
};
"""
    assert parse(hpp, extension) == [
        model.Struct('X', [
            model.StructMember('b', 'i8')
        ])
    ]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_struct_with_incomplete_array_in_file_with_hyphen(if_clang_installed, extension):
    hpp = """\
struct X
{
    struct
    {
        char a;
    } a;
};
"""
    nodes = parse(hpp, extension)

    assert '__test__' + extension[1:] + '__' in nodes[0].name


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_forward_declared_struct(if_clang_installed, extension):
    hpp = """\
struct X;
"""
    assert parse(hpp, extension) == []


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_omit_bitfields(if_clang_installed, extension):
    hpp = """\
struct X
{
    unsigned a: 1;
    unsigned b: 1;
    unsigned c: 1;
    unsigned  : 5;
};
"""
    assert parse(hpp, extension) == [model.Struct('X', [])]


class WarnMock(object):
    def __init__(self):
        self.warnings = []

    def __call__(self, msg, location='prophyc'):
        self.warnings.append((location, msg))


@pytest.mark.parametrize('extension, expected', [
    ('.c', 'type specifier missing, defaults to \'int\''),
    ('.cpp', 'C++ requires a type specifier for all declarations'),
])
def test_diagnostics_error(if_clang_installed, extension, expected):
    content = """\
unknown;
"""
    warn = WarnMock()

    assert parse(content,
                 extension,
                 warn=warn) == []
    assert warn.warnings == [('test' + extension + ':1:1', expected)]


@pytest.mark.parametrize('extension', [('.c'), ('.cpp')])
def test_diagnostics_warning(if_clang_installed, extension):
    content = """\
int foo()
{
    int x;
}
"""
    warn = WarnMock()

    assert parse(content,
                 extension,
                 warn=warn) == []
    assert warn.warnings == [('test' + extension + ':4:1', 'control reaches end of non-void function')]


def test_libclang_parsing_error(if_clang_installed, ):
    with pytest.raises(model.ParseError) as e:
        parse('content', '')
    assert e.value.errors == [('test', 'error parsing translation unit')]


@pytest.mark.parametrize('extension', [('.h'), ('.hpp')])
def test_include_dirs(if_clang_installed, extension, tmpdir):
    dependency_hpp = '''\
typedef double Double;
'''
    hpp = '''\
#include <dependency.hpp>
struct X
{
    Double x;
};
'''
    include_dir = tmpdir.join('include')

    include_dir.join('dependency.hpp').write(dependency_hpp, ensure=True)

    assert parse(hpp, extension, includes=[str(include_dir)]) == [model.Struct("X", [
        model.StructMember("x", "r64")
    ])]
