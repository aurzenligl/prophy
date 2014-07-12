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

def test_error_typedef_type_not_there():
    with pytest.raises(Exception) as e:
        parse('typedef x y;')
    assert "Name 'x' was not declared" in e.value.message

def test_error_typedef_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('typedef bytes x;')
    assert "Syntax error in input at 'bytes '" in e.value.message