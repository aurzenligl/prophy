from prophyc import model
from prophyc.parsers.prophy import ProphyParser

def parse(content):
    return ProphyParser().parse_string(content)

def test_constants_parsing():
    content = """\
const CONST_A = 0;
const CONST_B = 31;
"""

    assert parse(content) == [
        model.Constant("CONST_A", "0"),
        model.Constant("CONST_B", "31")
    ]
