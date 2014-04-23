import tempfile
import SackParser

def parse(content):
    with tempfile.NamedTemporaryFile(suffix = '.hpp') as temp:
        temp.write(content)
        temp.flush()
        return SackParser.SackParser().parse(temp.name)

def test_x():
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

# struct simple
# struct typedefed
# struct with struct (in namespace, typedefed)
# struct with nested typedefs
# struct with all ints
# struct with array
# struct with enum
# struct with union
