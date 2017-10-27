import prophyc
import pytest
import os


@pytest.clang_installed
def test_sack_includes_isar(tmpdir_cwd, tmpfiles_cwd):

    test_files = tmpfiles_cwd("included_by_isar.xml",
                              "included_by_sack.xml",
                              "included_by_sack.py",
                              "the_sack.cpp",
                              "the_sack.py")

    xml, xml2, xml2_py, cpp, py = test_files

    xml.write("""\
<x>
    <definitions>
         <typedef comment="some comment" name="IsarDefA" type="r32"/>
    </definitions>
    <struct name="IsarB">
        <member name="i_tdf" type="u16"/>
        <member name="y" type="u8">
            <dimension isVariableSize="true"/>
        </member>
    </struct>
</x>
""")
    xml2.write("""\
<x>
    <include href="included_by_isar.xml"/>
    <struct name="IsarA">
        <member name="i_A_a" type="u8"/>
        <member name="i_A_B" type="IsarB"/>
    </struct>
    <struct name="IsarV">
        <member name="i_V" type="u8">
            <dimension isVariableSize="true"/>
        </member>
    </struct>
</x>
""")

    cpp.write("""\
#include <stdint.h>
struct cppX
{
    IsarA defined_in_xml;
    IsarB defined_deeper_in_xmls;
    uint16_t regular_type;
    IsarDefA typedefed_deeper_in_xmls;
};
""")
    prophyc.main(["--sack", "--include_isar", str(xml2),
                  "--python_out", str(tmpdir_cwd), str(cpp)])

    assert all((os.path.isfile(str(f)) for f in test_files)), "Some files not created"

    assert xml2_py.read() == """\
import prophy

from included_by_isar import *

class IsarA(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('i_A_a', prophy.u8),
                   ('i_A_B', IsarB)]

class IsarV(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('i_V_len', prophy.u32),
                   ('i_V', prophy.array(prophy.u8, bound = 'i_V_len'))]
"""
    assert py.read() == """\
import prophy

from included_by_sack import *

class cppX(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('defined_in_xml', IsarA),
                   ('defined_deeper_in_xmls', IsarB),
                   ('regular_type', prophy.u16),
                   ('typedefed_deeper_in_xmls', IsarDefA)]
"""
