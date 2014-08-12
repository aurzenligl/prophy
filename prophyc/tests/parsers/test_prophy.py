import pytest

from prophyc import model
from prophyc.parsers.prophy import ProphyParser, ParseError

def parse(content):
    return ProphyParser().parse_string(content)

def test_constants_parsing():
    content = """\
const CONST_A = 31;
const CONST_B = 0x31;
const CONST_C = 031;
const CONST_D = -1;
"""

    assert parse(content) == [
        model.Constant("CONST_A", "31"),
        model.Constant("CONST_B", "0x31"),
        model.Constant("CONST_C", "031"),
        model.Constant("CONST_D", "-1")
    ]

#def test_typedefs_parsing():
#    content = """\
#typedef u32 x;
#typedef x y;
#"""
#
#    assert parse(content) == [
#        model.Typedef("x", "u32"),
#        model.Typedef("y", "x")
#    ]
#
#def test_enums_parsing():
#    content = """\
#enum enum_t
#{
#    enum_t_1 = 1,
#    enum_t_2 = 2,
#    enum_t_3 = enum_t_2
#};
#enum enum2_t
#{
#    enum2_t_1 = enum_t_3
#};
#"""
#
#    assert parse(content) == [
#        model.Enum('enum_t', [
#            model.EnumMember('enum_t_1', '1'),
#            model.EnumMember('enum_t_2', '2'),
#            model.EnumMember('enum_t_3', 'enum_t_2')
#        ]),
#        model.Enum('enum2_t', [
#            model.EnumMember('enum2_t_1', 'enum_t_3')
#        ])
#    ]
#
#def test_structs_parsing():
#    content = """\
#struct test
#{
#    u32 x;
#    u32 y;
#};
#"""
#    assert parse(content) == [
#        model.Struct('test', [
#            model.StructMember('x', 'u32'),
#            model.StructMember('y', 'u32')
#        ])
#    ]
#
#def test_structs_with_fixed_array_parsing():
#    content = """\
#const max = 5;
#struct test
#{
#    u32 x[3];
#    u32 y[max];
#    bytes z[10];
#};
#"""
#
#    assert parse(content) == [
#        model.Constant('max', '5'),
#        model.Struct('test', [
#            model.StructMember('x', 'u32', size = '3'),
#            model.StructMember('y', 'u32', size = 'max'),
#            model.StructMember('z', 'byte', size = '10')
#        ])
#    ]
#
#def test_structs_with_dynamic_array_parsing():
#    content = """\
#typedef u32 x_t;
#struct test
#{
#    x_t x<>;
#    bytes y<>;
#};
#"""
#
#    assert parse(content) == [
#        model.Typedef('x_t', 'u32'),
#        model.Struct('test', [
#            model.StructMember('num_of_x', 'u32'),
#            model.StructMember('x', 'x_t', bound = 'num_of_x'),
#            model.StructMember('num_of_y', 'u32'),
#            model.StructMember('y', 'byte', bound = 'num_of_y')
#        ])
#    ]
#
#def test_structs_with_limited_array_parsing():
#    content = """\
#enum sizes
#{
#    size = 10
#};
#struct test
#{
#    u32 x<5>;
#    u32 y<size>;
#};
#"""
#
#    assert parse(content) == [
#        model.Enum('sizes', [
#            model.EnumMember('size', '10')
#        ]),
#        model.Struct('test', [
#            model.StructMember('num_of_x', 'u32'),
#            model.StructMember('x', 'u32', bound = 'num_of_x', size = '5'),
#            model.StructMember('num_of_y', 'u32'),
#            model.StructMember('y', 'u32', bound = 'num_of_y', size = 'size')
#        ])
#    ]
#
#def test_structs_with_greedy_array_parsing():
#    content = """\
#struct test
#{
#    u32 x<...>;
#};
#"""
#
#    assert parse(content) == [
#        model.Struct('test', [
#            model.StructMember('x', 'u32', unlimited = True)
#        ])
#    ]
#
#def test_structs_with_optional_field():
#    content = """\
#struct test
#{
#    u32* x;
#};
#"""
#
#    assert parse(content) == [
#        model.Struct('test', [
#            model.StructMember('x', 'u32', optional = True)
#        ])
#    ]
#
#def test_unions_parsing():
#    content = """\
#const three = 3;
#typedef u32 z_t;
#union test
#{
#    1: u32 x;
#    2: u32 y;
#    three: z_t z;
#};
#"""
#
#    assert parse(content) == [
#        model.Constant('three', '3'),
#        model.Typedef('z_t', 'u32'),
#        model.Union('test', [
#            model.UnionMember('x', 'u32', '1'),
#            model.UnionMember('y', 'u32', '2'),
#            model.UnionMember('z', 'z_t', 'three')
#        ])
#    ]
#
#def test_floats_parsing():
#    content = """\
#typedef float x;
#typedef double y;
#struct z { float a; double b; };
#"""
#
#    assert parse(content) == [
#        model.Typedef('x', 'r32'),
#        model.Typedef('y', 'r64'),
#        model.Struct('z', [
#            model.StructMember('a', 'r32'),
#            model.StructMember('b', 'r64')
#        ])
#    ]
#
#def test_error_lack_of_semicolon():
#    with pytest.raises(ParseError) as e:
#        parse('const CONST = 0')
#    assert "Could not create parse tree!" in e.value.message
#
#def test_error_newline_in_type_definition():
#    with pytest.raises(ParseError) as e:
#        parse('const \nCONST = 0;')
#    assert "Syntax error in input at '\n'" in e.value.message
#
#def test_no_error_with_newlines():
#    assert len(parse('\nconst CONST1 = 0;\n\r\nconst CONST2 = 0;\n')) == 2
#
#def test_no_error_with_comments():
#    assert len(parse("""\
#const CONST1 = 0; // ajisja /* */
#const CONST2 = 0; //// ajisja
#// odkosd
#// const CONST3 = 0;
#/*
#const CONST4 = 0; /// ajisja
#*/
#const CONST5 = 0;
#""")) == 3
#
#def test_error_constant_text_value():
#    with pytest.raises(ParseError) as e:
#        parse('const CONST_X = wrong;')
#    assert "Syntax error in input at 'wrong'" in e.value.message
#
#def test_error_constant_redefined():
#    with pytest.raises(Exception) as e:
#        parse('const CONST = 1; const CONST_DIFFERENT = 1; const CONST = 1;')
#    assert "Name 'CONST' redefined" in e.value.message
#
#def test_error_constant_builtin_as_identifier():
#    with pytest.raises(ParseError) as e:
#        parse('const u32 = 0;')
#    assert "Syntax error in input at 'u32 '" in e.value.message
#    with pytest.raises(ParseError) as e:
#        parse('const bytes = 0;')
#    assert "Syntax error in input at 'bytes '" in e.value.message
#
#def test_error_typedef_redefined():
#    with pytest.raises(Exception) as e:
#        parse('typedef u32 x; typedef u32 x;')
#    assert "Name 'x' redefined" in e.value.message
#
#def test_error_typedef_type_not_declared():
#    with pytest.raises(Exception) as e:
#        parse('typedef x y;')
#    assert "Type 'x' was not declared" in e.value.message
#
#def test_error_typedef_builtin_as_identifier():
#    with pytest.raises(ParseError) as e:
#        parse('typedef bytes x;')
#    assert "Syntax error in input at 'bytes '" in e.value.message
#    with pytest.raises(ParseError) as e:
#        parse('typedef u32 bytes ;')
#    assert "Syntax error in input at 'bytes '" in e.value.message
#
#def test_error_enum_builtin_as_identifier():
#    with pytest.raises(ParseError) as e:
#        parse('enum u32 { enum_t_1 = 1 };')
#    assert "Syntax error in input at 'u32 '" in e.value.message
#    with pytest.raises(ParseError) as e:
#        parse('enum enum_t { u32 = 1 };')
#    assert "Syntax error in input at 'u32 '" in e.value.message
#    with pytest.raises(ParseError) as e:
#        parse('enum enum_t { enum_t_1 = u32 };')
#    assert "Syntax error in input at 'u32 '" in e.value.message
#
#def test_error_enum_redefined():
#    with pytest.raises(Exception) as e:
#        parse('const enum_t = 10; enum enum_t { enum_t_1 = 1 };')
#    assert "Name 'enum_t' redefined" in e.value.message
#    with pytest.raises(Exception) as e:
#        parse('const enum_t_1 = 10; enum enum_t { enum_t_1 = 1 };')
#    assert "Name 'enum_t_1' redefined" in e.value.message
#    with pytest.raises(Exception) as e:
#        parse('enum enum_t { enum_t_1 = 1 }; const enum_t_1 = 10; ')
#    assert "Name 'enum_t_1' redefined" in e.value.message
#
#def test_error_enum_constant_not_declared():
#    with pytest.raises(Exception) as e:
#        parse('enum enum_t { enum_t_1 = unknown };')
#    assert "Constant 'unknown' was not declared" in e.value.message
#
#def test_no_error_enum_comment():
#    assert len(parse('enum enum_t { enum_t_1 = 1, /* xxx */ enum_t_2 = 2 };')) == 1
#
#def test_error_struct_redefined():
#    with pytest.raises(Exception) as e:
#        parse('const test = 10; struct test { u32 x; };')
#    assert "Name 'test' redefined" in e.value.message
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x; }; struct test { u32 x; };')
#    assert "Name 'test' redefined" in e.value.message
#
#def test_error_struct_empty():
#    with pytest.raises(ParseError) as e:
#        parse('struct test {};')
#    assert "Syntax error in input at '}'" in e.value.message
#
#def test_error_struct_repeated_field_names():
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x; u32 x; };')
#    assert "Field 'x' redefined" in e.value.message
#
#def test_no_error_struct_comments_between_newlines():
#    assert len(parse('struct test { u32 x; /* \n u32 y; \n */ \n u32 z; };')) == 1
#    assert len(parse('struct test { u32 x; // xxxx \n u32 y; \n // u32 z; \n };')) == 1
#
#def test_error_struct_field_type_not_declared():
#    with pytest.raises(Exception) as e:
#        parse('struct test { unknown x; };')
#    assert "Type 'unknown' was not declared" in e.value.message
#
#def test_error_struct_array_size_not_declared():
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x[unknown]; };')
#    assert "Constant 'unknown' was not declared" in e.value.message
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x<unknown>; };')
#    assert "Constant 'unknown' was not declared" in e.value.message
#
#def test_error_struct_array_size_cannot_be_negative():
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x[-1]; };')
#    assert "Array size '-1' must be positive" in e.value.message
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x<0>; };')
#    assert "Array size '0' must be positive" in e.value.message
#
#def test_error_struct_greedy_field_is_not_the_last_one():
#    with pytest.raises(Exception) as e:
#        parse('struct test { u32 x<...>; u32 y; };')
#    assert "Greedy array field 'x' not last" in e.value.message
#
#def test_error_union_redefined():
#    with pytest.raises(Exception) as e:
#        parse('const test = 10; union test { 1: u32 x; };')
#    assert "Name 'test' redefined" in e.value.message
#    with pytest.raises(Exception) as e:
#        parse('union test { 1: u32 x; }; union test { 1: u32 x; };')
#    assert "Name 'test' redefined" in e.value.message
#
#def test_error_union_empty():
#    with pytest.raises(ParseError) as e:
#        parse('union test {};')
#    assert "Syntax error in input at '}'" in e.value.message
#
#def test_error_union_repeated_arm_name():
#    with pytest.raises(Exception) as e:
#        parse('union test { 1: u32 x; 2: u32 x; };')
#    assert "Field 'x' redefined" in e.value.message
#
#def test_error_union_repeated_arm_discriminator():
#    with pytest.raises(Exception) as e:
#        parse('union test { 1: u32 x; 2: u32 x; };')
#    assert "Field 'x' redefined" in e.value.message
#
#def test_error_union_field_type_not_declared():
#    with pytest.raises(Exception) as e:
#        parse('union test { 1: u32 x; 1: u32 y; };')
#    assert "Value '1' redefined" in e.value.message
#
#def test_error_union_discriminator_size_not_declared():
#    with pytest.raises(Exception) as e:
#        parse('union test { unknown: u32 x; };')
#    assert "Constant 'unknown' was not declared" in e.value.message
