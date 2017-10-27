
from prophyc import model
import pytest
import os


def test_isar_patch(call, tmpdir_cwd):
    xml = tmpdir_cwd.join("input.xml")
    cpp = tmpdir_cwd.join("input.cpp")
    py = tmpdir_cwd.join("input.py")
    xml.write("""\
<x>
    <definitions>
         <typedef comment="some comment" name="DefA" type="u16"/>
    </definitions>
    <struct name="B">
        <member name="a" type="u16"/>
    </struct>
    <struct name="A">
        <member name="a" type="u8"/>
    </struct>
</x>
""")

    cpp.write("""\
#include <stdint.h>
struct X
{
    DefA a;
    B b;
    uint32_t c;
};
""")
    ret, out, err = call(["--sack", "--include_isar", str(xml),
                          "--python_out", str(tmpdir_cwd), str(cpp)])
    print out
    print err
    print py.read()
    assert ret == 0
    