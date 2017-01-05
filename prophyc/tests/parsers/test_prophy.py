import pytest

from prophyc import model
from prophyc.model import ParseError
from prophyc.parsers.prophy import ProphyParser
from prophyc.file_processor import CyclicIncludeError, FileNotFoundError

def parse(content, parse_file = lambda path: []):
    return ProphyParser().parse(content, 'test.prophy', parse_file)

def test_constants_parsing():
    content = """\
const CONST_A = 31;
const CONST_B = 0x31;
const CONST_C = 031;
const CONST_D = -1;
"""

    assert parse(content) == [
        model.Constant("CONST_A", "31"),
        model.Constant("CONST_B", "49"),
        model.Constant("CONST_C", "25"),
        model.Constant("CONST_D", "-1")
    ]

def test_constant_expressions():
    content = """\
const A = 1;
const B = A * 2;
const C = (B - A) * 3;
const D = -C;
const E = D << 2;
"""

    assert parse(content) == [
        model.Constant("A", "1"),
        model.Constant("B", "2"),
        model.Constant("C", "3"),
        model.Constant("D", "-3"),
        model.Constant("E", "-12")
    ]

def test_constant_expressions_errors():
    content = """\
const A = 2 + C;
const B = -D;
const C = 1 / 0;
"""
    with pytest.raises(ParseError) as e:
        parse(content)
    assert e.value.errors == [
        ("test.prophy:1:15", "constant 'C' was not declared"),
        ("test.prophy:2:12", "constant 'D' was not declared"),
        ("test.prophy:3:11", "division by zero")
    ]

def test_constant_with_newline():
    assert parse("const \nCONST = 0;") == [model.Constant("CONST", "0")]

def test_typedefs_parsing():
    content = """\
typedef u32 x;
typedef x y;
"""

    assert parse(content) == [
        model.Typedef("x", "u32"),
        model.Typedef("y", "x")
    ]

def test_enums_parsing():
    content = """\
enum enum_t
{
    enum_t_1 = 1,
    enum_t_2 = 2,
    enum_t_3 = enum_t_2
};
enum enum2_t
{
    enum2_t_1 = enum_t_3
};
"""

    assert parse(content) == [
        model.Enum('enum_t', [
            model.EnumMember('enum_t_1', '1'),
            model.EnumMember('enum_t_2', '2'),
            model.EnumMember('enum_t_3', '2')
        ]),
        model.Enum('enum2_t', [
            model.EnumMember('enum2_t_1', '2')
        ])
    ]

def test_structs_parsing():
    content = """\
struct test
{
    u32 x;
    u32 y;
};
"""
    assert parse(content) == [
        model.Struct('test', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ])
    ]

def test_structs_with_fixed_array_parsing():
    content = """\
const max = 5;
struct test
{
    u32 x[3];
    u32 y[max];
    bytes z[10];
};
"""

    assert parse(content) == [
        model.Constant('max', '5'),
        model.Struct('test', [
            model.StructMember('x', 'u32', size = '3'),
            model.StructMember('y', 'u32', size = '5'),
            model.StructMember('z', 'byte', size = '10')
        ])
    ]

def test_structs_with_dynamic_array_parsing():
    content = """\
typedef u32 x_t;
struct test
{
    x_t x<>;
    bytes y<>;
};
"""

    assert parse(content) == [
        model.Typedef('x_t', 'u32'),
        model.Struct('test', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'x_t', bound = 'num_of_x'),
            model.StructMember('num_of_y', 'u32'),
            model.StructMember('y', 'byte', bound = 'num_of_y')
        ])
    ]

def test_structs_with_dynamic_arrays_bounded_by_the_same_member_parsing():
    content = """\
typedef u32 x_t;
struct test
{
    u32 num_of_elements;
    u16 dummy;
    x_t x<@num_of_elements>;
    bytes y<@num_of_elements>;
};
"""

    assert parse(content) == [
        model.Typedef('x_t', 'u32'),
        model.Struct('test', [
            model.StructMember('num_of_elements', 'u32'),
            model.StructMember('dummy', 'u16'),
            model.StructMember('x', 'x_t', bound = 'num_of_elements'),
            model.StructMember('y', 'byte', bound = 'num_of_elements')
        ])
    ]

def test_structs_with_dynamic_arrays_bounded_by_the_same_member_parsing_typedef_sizer():
    content = """\
typedef i32 num_of_elements_t;
typedef num_of_elements_t sz_t;
struct ExtSized
{
    sz_t sz;
    u32 one<@sz>;
    u16 two<@sz>;
    i32 three<@sz>;
};
"""

    assert parse(content) == [
        model.Typedef('num_of_elements_t', 'i32'),
        model.Typedef('sz_t', 'num_of_elements_t'),
        model.Struct('ExtSized', [
            model.StructMember('sz', 'sz_t'),
            model.StructMember('one', 'u32', bound = 'sz'),
            model.StructMember('two', 'u16', bound = 'sz'),
            model.StructMember('three', 'i32', bound = 'sz')
        ])
    ]

def test_structs_with_limited_array_parsing():
    content = """\
enum sizes
{
    size = 10
};
struct test
{
    u32 x<5>;
    u32 y<size>;
};
"""

    assert parse(content) == [
        model.Enum('sizes', [
            model.EnumMember('size', '10')
        ]),
        model.Struct('test', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x', size = '5'),
            model.StructMember('num_of_y', 'u32'),
            model.StructMember('y', 'u32', bound = 'num_of_y', size = '10')
        ])
    ]

def test_structs_with_greedy_array_parsing():
    content = """\
struct test
{
    u32 x<...>;
};
"""

    assert parse(content) == [
        model.Struct('test', [
            model.StructMember('x', 'u32', unlimited = True)
        ])
    ]

def test_structs_with_optional_field():
    content = """\
struct test
{
    u32* x;
};
"""

    assert parse(content) == [
        model.Struct('test', [
            model.StructMember('x', 'u32', optional = True)
        ])
    ]

def test_unions_parsing():
    content = """\
const three = 3;
typedef u32 z_t;
union test
{
    1: u32 x;
    2: u32 y;
    three: z_t z;
};
"""

    assert parse(content) == [
        model.Constant('three', '3'),
        model.Typedef('z_t', 'u32'),
        model.Union('test', [
            model.UnionMember('x', 'u32', '1'),
            model.UnionMember('y', 'u32', '2'),
            model.UnionMember('z', 'z_t', '3')
        ])
    ]

def test_floats_parsing():
    content = """\
typedef float x;
typedef double y;
struct z { float a; double b; };
"""

    assert parse(content) == [
        model.Typedef('x', 'r32'),
        model.Typedef('y', 'r64'),
        model.Struct('z', [
            model.StructMember('a', 'r32'),
            model.StructMember('b', 'r64')
        ])
    ]

def test_lexer_error():
    with pytest.raises(ParseError) as e:
        parse('const ?')
    assert ":1:7", "illegal character '?'" == e.value.errors[0]

def test_syntax_error():
    with pytest.raises(ParseError) as e:
        parse('const CONST badtoken')
    assert ":1:13", "syntax error at 'badtoken'" == e.value.errors[0]

def test_unexpected_end_of_input():
    with pytest.raises(ParseError) as e:
        parse('const CONST = 0')
    assert ":1:15", "unexpected end of input" == e.value.errors[0]

def test_no_error_with_newlines():
    assert len(parse('\nconst CONST1 = 0;\n\r\nconst CONST2 = 0;\n')) == 2

def test_no_error_with_comments():
    assert len(parse("""\
const CONST1 = 0; // ajisja /* */
const CONST2 = 0; //// ajisja
// odkosd
// const CONST3 = 0;
/*
const CONST4 = 0; /// ajisja
*/
const CONST5 = 0;
""")) == 3

def test_error_constant_text_value():
    with pytest.raises(ParseError) as e:
        parse('const CONST_X = wrong;')
    assert ":1:17", "constant 'wrong' was not declared" == e.value.errors[0]

def test_error_constant_redefined():
    with pytest.raises(ParseError) as e:
        parse('const CONST = 1; const CONST_DIFFERENT = 1; const CONST = 1;')
    assert ":1:51", "name 'CONST' redefined" == e.value.errors[0]

def test_error_constant_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('const u32 = 0;')
    assert ":1:7", "syntax error at 'u32'" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('const bytes = 0;')
    assert ":1:7", "syntax error at 'bytes'" == e.value.errors[0]

def test_error_typedef_redefined():
    with pytest.raises(ParseError) as e:
        parse('typedef u32 x; typedef u32 x;')
    assert ":1:28", "name 'x' redefined" == e.value.errors[0]

def test_error_typedef_type_not_declared():
    with pytest.raises(ParseError) as e:
        parse('typedef x y;')
    assert ":1:9", "type 'x' was not declared" == e.value.errors[0]

def test_error_typedef_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('typedef bytes x;')
    assert ":1:9", "syntax error at 'bytes'" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('typedef u32 bytes;')
    assert ":1:13", "syntax error at 'bytes'" == e.value.errors[0]

def test_error_enum_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('enum u32 { enum_t_1 = 1 };')
    assert ":1:6", "syntax error at 'u32'" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('enum enum_t { u32 = 1 };')
    assert ":1:15", "syntax error at 'u32'" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('enum enum_t { enum_t_1 = u32 };')
    assert ":1:26", "syntax error at 'u32'" == e.value.errors[0]

def test_error_enum_redefined():
    with pytest.raises(ParseError) as e:
        parse('const enum_t = 10; enum enum_t { enum_t_1 = 1 };')
    assert ":1:25", "name 'enum_t' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('const enum_t_1 = 10; enum enum_t { enum_t_1 = 1 };')
    assert ":1:36", "name 'enum_t_1' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('enum enum_t { enum_t_1 = 1 }; const enum_t_1 = 10; ')
    assert ":1:37", "name 'enum_t_1' redefined" == e.value.errors[0]

def test_error_enum_constant_not_declared():
    with pytest.raises(ParseError) as e:
        parse('enum enum_t { enum_t_1 = unknown };')
    assert ":1:26", "constant 'unknown' was not declared" == e.value.errors[0]

def test_no_error_enum_comment():
    assert len(parse('enum enum_t { enum_t_1 = 1, /* xxx */ enum_t_2 = 2 };')) == 1

def test_error_struct_redefined():
    with pytest.raises(ParseError) as e:
        parse('const test = 10; struct test { u32 x; };')
    assert ":1:25", "name 'test' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x; }; struct test { u32 x; };')
    assert ":1:32", "name 'test' redefined" == e.value.errors[0]

def test_error_struct_empty():
    with pytest.raises(ParseError) as e:
        parse('struct test {};')
    assert ":1:14", "syntax error at '}'" == e.value.errors[0]

def test_error_struct_empty_2():
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 <@b>;};')
    assert ":1:14", "syntax error at '}'" == e.value.errors[0]

def test_error_struct_repeated_field_names():
    with pytest.raises(ParseError) as e:
        parse("""\
struct test
{
    u32 x;
    u32 x;
};""")
    assert ":4:9", "field 'x' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse("""\
struct test
{
    u32 num_of_x;
    u32 x<>;
};""")
    assert ":4:9", "field 'num_of_x' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse("""\
struct test
{
    u32 x<>;
    u32 num_of_x;
};""")
    assert ":4:9", "field 'num_of_x' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse("""\
struct test
{
    u8 a;
    u32 x<@a>;
    u32 x<@a>;
};""")
    assert ":4:9", "field 'x' redefined" == e.value.errors[0]

def test_no_error_struct_comments_between_newlines():
    assert len(parse('struct test { u32 x; /* \n u32 y; \n */ \n u32 z; };')) == 1
    assert len(parse('struct test { u32 x; // xxxx \n u32 y; \n // u32 z; \n };')) == 1

def test_error_struct_field_type_not_declared():
    with pytest.raises(ParseError) as e:
        parse('struct test { unknown x; };')
    assert ":1:15", "type 'unknown' was not declared" == e.value.errors[0]

def test_error_struct_array_size_not_declared():
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x[unknown]; };')
    assert ":1:21", "constant 'unknown' was not declared" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x<unknown>; };')
    assert ":1:21", "constant 'unknown' was not declared" == e.value.errors[0]

def test_error_struct_array_size_cannot_be_negative():
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x[-1]; };')
    assert ":1:21", "array size '-1' non-positive" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x<0>; };')
    assert ":1:21", "array size '0' non-positive" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x[(0)]; };')
    assert ":1:21", "array size '0' non-positive" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('const X = -2; struct test { u32 x[X]; };')
    assert ":1:35", "array size '-2' non-positive" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x[1-2]; };')
    assert ":1:21", "array size '-1' non-positive" == e.value.errors[0]

def test_error_struct_sizer_of_dynamic_array_is_not_defined_before():
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x<@sz>; u32 sz; };')
    assert ":1:19", "Sizer of 'x' has to be defined before the array" == e.value.errors[0]

    with pytest.raises(ParseError) as e:
        parse('const sz = 10; struct test { u32 x<@sz>;};')
    assert ":1:34", "Sizer of 'x' has to be defined before the array" == e.value.errors[0]

def test_error_struct_sizer_of_dynamic_array_is_not_of_integer_type():
    with pytest.raises(ParseError) as e:
        parse('struct X { u32 s; }; struct test { X sz; u32 x<@sz>; };')
    assert ":1:46", "Sizer of 'x' has to be of (unsigned) integer type" == e.value.errors[0]

def test_error_struct_greedy_field_is_not_the_last_one():
    with pytest.raises(ParseError) as e:
        parse('struct test { u32 x<...>; u32 y; };')
    assert ":1:19", "greedy array field 'x' not last" == e.value.errors[0]

def test_error_union_redefined():
    with pytest.raises(ParseError) as e:
        parse('const test = 10; union test { 1: u32 x; };')
    assert ":1:24", "name 'test' redefined" == e.value.errors[0]
    with pytest.raises(ParseError) as e:
        parse('union test { 1: u32 x; }; union test { 1: u32 x; };')
    assert ":1:33", "name 'test' redefined" == e.value.errors[0]

def test_error_union_empty():
    with pytest.raises(ParseError) as e:
        parse('union test {};')
    assert ":1:13", "syntax error at '}'" == e.value.errors[0]

def test_error_union_repeated_arm_name():
    with pytest.raises(ParseError) as e:
        parse('union test { 1: u32 x; 2: u32 x; };')
    assert ":1:31", "field 'x' redefined" == e.value.errors[0]

def test_error_union_repeated_arm_discriminator():
    with pytest.raises(ParseError) as e:
        parse('union test { 1: u32 x; 1: u32 y; };')
    assert ":1:31", "duplicate discriminator value '1'" == e.value.errors[0]

def test_error_union_field_type_not_declared():
    with pytest.raises(ParseError) as e:
        parse('union test { 1: dontknow x };')
    assert ":1:17", "type 'dontknow' was not declared" == e.value.errors[0]

def test_error_union_discriminator_not_declared():
    with pytest.raises(ParseError) as e:
        parse('union test { unknown: u32 x; };')
    assert ":1:14", "constant 'unknown' was not declared" == e.value.errors[0]

def test_multiple_errors():
    with pytest.raises(ParseError) as e:
        parse("""\
struct X { u32 x; u32 x; };
union Y { unknown: u32 x; };
const Z 2;
""")
    assert e.value.errors == [
        ("test.prophy:1:23", "field 'x' redefined"),
        ("test.prophy:2:11", "constant 'unknown' was not declared"),
        ("test.prophy:3:9", "syntax error at '2'")
    ]

def test_typedef_cross_referenced_definition():
    typedef = parse("struct X { u32 x; }; typedef X Y;")[1]
    assert type(typedef.definition) == model.Struct
    assert typedef.definition.name == 'X'

def test_struct_member_cross_referenced_definition():
    members = parse("""\
typedef u32 X;
struct Y
{
    X x1;
    X* x2;
    X x3[1];
    X x5<1>;
    X x4<>;
    X x6<@x1>;
    X x7<...>;
};
""")[1].members
    assert type(members[0].definition) == model.Typedef
    assert type(members[1].definition) == model.Typedef
    assert type(members[2].definition) == model.Typedef
    assert members[3].definition is None
    assert type(members[4].definition) == model.Typedef
    assert members[5].definition is None
    assert type(members[6].definition) == model.Typedef
    assert type(members[7].definition) == model.Typedef
    assert type(members[8].definition) == model.Typedef

def test_struct_kinds():
    structs = parse("""\
struct X1 { u32 x; };
struct X2 { u32 x<>; };
struct X3 { u32 x<...>; };
struct X4 { u8 a; u32 x<@a>; };
struct Y1 { X1 x; };
struct Y2 { X2 x; };
struct Y3 { X3 x; };
struct Y4 { X4 x; };
""")
    assert structs[0].kind == model.Kind.FIXED
    assert structs[1].kind == model.Kind.DYNAMIC
    assert structs[2].kind == model.Kind.UNLIMITED
    assert structs[3].kind == model.Kind.DYNAMIC
    assert structs[4].kind == model.Kind.FIXED
    assert structs[5].kind == model.Kind.DYNAMIC
    assert structs[6].kind == model.Kind.UNLIMITED
    assert structs[7].kind == model.Kind.DYNAMIC
    assert structs[0].members[0].kind == model.Kind.FIXED
    assert structs[1].members[0].kind == model.Kind.FIXED
    assert structs[2].members[0].kind == model.Kind.FIXED
    assert structs[3].members[0].kind == model.Kind.FIXED
    assert structs[3].members[1].kind == model.Kind.FIXED
    assert structs[4].members[0].kind == model.Kind.FIXED
    assert structs[5].members[0].kind == model.Kind.DYNAMIC
    assert structs[6].members[0].kind == model.Kind.UNLIMITED
    assert structs[7].members[0].kind == model.Kind.DYNAMIC

def test_error_struct_non_last_field_has_unlimited_kind():
    with pytest.raises(ParseError) as e:
        parse("struct X { u32 x<...>; }; struct Y { X x; u32 y; };")
    assert ":1:40", "greedy array field 'x' not last" == e.value.errors[0]

def test_error_union_member_has_dynamic_kind():
    with pytest.raises(ParseError) as e:
        parse("struct X { u32 x<>; }; union Y { 0: X x; };")
    assert ":1:39", "dynamic union arm 'x'" == e.value.errors[0]

def test_error_union_member_has_unlimited_kind():
    with pytest.raises(ParseError) as e:
        parse("struct X { u32 x<...>; }; union Y { 0: X x; };")
    assert ":1:42", "dynamic union arm 'x'" == e.value.errors[0]

def test_include_path():
    assert parse('#include "x.prophy"') == [model.Include('x', [])]
    assert parse('#include "noext"') == [model.Include('noext', [])]
    assert parse('#include "102.prophy"') == [model.Include('102', [])]
    assert parse('#include "x/y/z.prophy"') == [model.Include('z', [])]
    assert parse('#include "./x.prophy"') == [model.Include('x', [])]
    assert parse('#include "../x.prophy"') == [model.Include('x', [])]
    assert parse('#include "x.y.z.prophy"') == [model.Include('x.y.z', [])]
    assert parse(' # include  "x.prophy" ') == [model.Include('x', [])]
    assert parse('\n#\ninclude\n"x.prophy"\n') == [model.Include('x', [])]

def test_include_path_errors():
    with pytest.raises(ParseError) as e:
        parse('#notinclude "test"')
    assert e.value.errors == [("test.prophy:1:2", "unknown directive 'notinclude'")]
    with pytest.raises(ParseError) as e:
        parse('#include <test>')
    assert e.value.errors == [("test.prophy:1:10", "syntax error at '<'")]

def test_include_no_error_with_constant():
    content = """\
#include "test.prophy"
const Y = X;
"""
    parse(content, lambda path: [model.Constant('X', '42')])

def test_include_no_error_with_typedef():
    content = """\
#include "test.prophy"
typedef X Y;
"""
    parse(content, lambda path: [model.Typedef('X', 'u32')])

def test_include_no_error_with_enum():
    content = """\
#include "test.prophy"
typedef X Y;
const Z = X1;
"""
    parse(content, lambda path: [model.Enum('X', [model.EnumMember('X1', '1')])])

def test_include_no_error_with_struct():
    content = """\
#include "test.prophy"
typedef X Y;
"""
    parse(content, lambda path: [model.Struct('X', [])])

def test_include_no_error_with_union():
    content = """\
#include "test.prophy"
typedef X Y;
"""
    parse(content, lambda path: [model.Union('X', [])])

def test_include_errors():
    with pytest.raises(ParseError) as e:
        def parse_file(path):
            raise FileNotFoundError(path)
        parse('#include "imnotthere"', parse_file)
    assert e.value.errors == [("test.prophy:1:10", "file imnotthere not found")]
    with pytest.raises(ParseError) as e:
        def parse_file(path):
            raise CyclicIncludeError(path)
        parse('#include "includemeagain"', parse_file)
    assert e.value.errors == [("test.prophy:1:10", "file includemeagain included again during parsing")]
