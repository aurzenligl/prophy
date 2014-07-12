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

def test_error_constant_text_value():
    with pytest.raises(ParseError) as e:
        parse('const CONST_X = wrong;')
    assert "Syntax error in input at 'wrong'" in e.value.message

def test_error_builtin_as_identifier():
    with pytest.raises(ParseError) as e:
        parse('const u32 = 0;')
    assert "Syntax error in input at 'u32 '" in e.value.message

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
