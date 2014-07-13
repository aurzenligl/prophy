import pytest

from prophyc import model
from prophyc.parsers.prophy import ProphyParser, ParseError

def parse(content):
    return ProphyParser().parse_string(content)

def test_constants_parsing():
    content = """\
const CONST_A = 31;
const CONST_B = 0x31;
const CONST_C = 0o31;
const CONST_D = 031;
const CONST_E = -1;
"""

    assert parse(content) == [
        model.Constant("CONST_A", "31"),
        model.Constant("CONST_B", "0x31"),
        model.Constant("CONST_C", "0o31"),
        model.Constant("CONST_D", "031"),
        model.Constant("CONST_E", "-1")
    ]

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
            model.EnumMember('enum_t_3', 'enum_t_2')
        ]),
        model.Enum('enum2_t', [
            model.EnumMember('enum2_t_1', 'enum_t_3')
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
            model.StructMember('x', 'u32', None, None, None, False),
            model.StructMember('y', 'u32', None, None, None, False)
        ])
    ]

def test_structs_with_fixed_array_parsing():
    content = """\
struct test
{
    u32 x[3];
};
"""

    assert parse(content) == [
        model.Struct('test', [
            model.StructMember('x', 'u32', True, None, '3', False)
        ])
    ]

def test_structs_with_dynamic_array_parsing():
    content = """\
struct test
{
    u32 x<>;
};
"""

    assert parse(content) == [
        model.Struct('test', [
            model.StructMember('num_of_x', 'u32', None, None, None, False),
            model.StructMember('x', 'u32', True, 'num_of_x', None, False)
        ])
    ]

def test_structs_with_limited_array_parsing():
    content = """\
struct test
{
    u32 x<5>;
};
"""

    assert parse(content) == [
        model.Struct('test', [
            model.StructMember('num_of_x', 'u32', None, None, None, False),
            model.StructMember('x', 'u32', True, 'num_of_x', '5', False)
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
            model.StructMember('x', 'u32', True, None, None, False)
        ])
    ]

def test_error_lack_of_semicolon():
    with pytest.raises(ParseError) as e:
        parse('const CONST = 0')
    assert "Could not create parse tree!" in e.value.message

def test_error_newline_in_type_definition():
    with pytest.raises(ParseError) as e:
        parse('const \nCONST = 0;')
    assert "Syntax error in input at '\n'" in e.value.message

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
    assert "Syntax error in input at 'wrong'" in e.value.message

def test_error_constant_redefined():
    with pytest.raises(Exception) as e:
        parse('const CONST = 1; const CONST_DIFFERENT = 1; const CONST = 1;')
    assert "Name 'CONST' redefined" in e.value.message

def test_error_constant_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('const u32 = 0;')
    assert "Syntax error in input at 'u32 '" in e.value.message
    with pytest.raises(ParseError) as e:
        parse('const bytes = 0;')
    assert "Syntax error in input at 'bytes '" in e.value.message

def test_error_typedef_redefined():
    with pytest.raises(Exception) as e:
        parse('typedef u32 x; typedef u32 x;')
    assert "Name 'x' redefined" in e.value.message

def test_error_typedef_type_not_declared():
    with pytest.raises(Exception) as e:
        parse('typedef x y;')
    assert "Type 'x' was not declared" in e.value.message

def test_error_typedef_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('typedef bytes x;')
    assert "Syntax error in input at 'bytes '" in e.value.message
    with pytest.raises(ParseError) as e:
        parse('typedef u32 bytes ;')
    assert "Syntax error in input at 'bytes '" in e.value.message

def test_error_enum_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('enum u32 { enum_t_1 = 1 };')
    assert "Syntax error in input at 'u32 '" in e.value.message
    with pytest.raises(ParseError) as e:
        parse('enum enum_t { u32 = 1 };')
    assert "Syntax error in input at 'u32 '" in e.value.message
    with pytest.raises(ParseError) as e:
        parse('enum enum_t { enum_t_1 = u32 };')
    assert "Syntax error in input at 'u32 '" in e.value.message

def test_error_enum_redefined():
    with pytest.raises(Exception) as e:
        parse('const enum_t = 10; enum enum_t { enum_t_1 = 1 };')
    assert "Name 'enum_t' redefined" in e.value.message
    with pytest.raises(Exception) as e:
        parse('const enum_t_1 = 10; enum enum_t { enum_t_1 = 1 };')
    assert "Name 'enum_t_1' redefined" in e.value.message
    with pytest.raises(Exception) as e:
        parse('enum enum_t { enum_t_1 = 1 }; const enum_t_1 = 10; ')
    assert "Name 'enum_t_1' redefined" in e.value.message

def test_error_enum_constant_not_declared():
    with pytest.raises(Exception) as e:
        parse('enum enum_t { enum_t_1 = unknown };')
    assert "Constant 'unknown' was not declared" in e.value.message

def test_no_error_enum_comment():
    assert len(parse('enum enum_t { enum_t_1 = 1, /* xxx */ enum_t_2 = 2 };')) == 1

def test_error_struct_repeated_field_names():
    pass

def test_no_error_struct_comments_between_newlines():
    pass
