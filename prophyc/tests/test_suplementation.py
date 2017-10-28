import prophyc
import pytest
import os

XML_1_CONTENT = """\
<x>
<definitions>
     <typedef comment="some comment" name="IsarDefA" type="r32"/>
     <typedef comment="some comment" name="IsarDefB" type="r32"/>
</definitions>
<struct name="IsarDefC">
    <member name="ifC_a" type="u16"/>
    <member name="ifC_b" type="u8">
        <dimension isVariableSize="true"/>
    </member>
</struct>
</x>
"""

XML_2_CONTENT = """\
<x>
<include href="included_by_isar.xml"/>
<struct name="IsarA">
    <member name="ifA_a" type="u8"/>
    <member name="ifA_B" type="IsarDefC"/>
</struct>
<struct name="IsarV">
    <member name="theItems" type="IsarDefB">
        <dimension isVariableSize="true" variableSizeFieldName="numOfItems"/>
    </member>
</struct>
</x>
"""


@pytest.clang_installed
def test_sack_includes_isar(tmpdir_cwd, tmpfiles_cwd):

    input_file_names = ("included_by_isar.xml",
                        "included_by_sack.xml",
                        "the_sack.cpp")

    xml, xml2, cpp = tmpfiles_cwd(*input_file_names)

    output_file_names = map(lambda f: os.path.splitext(f)[0] + '.py', input_file_names)
    xml_py, xml2_py, cpp_py = output_files = tmpfiles_cwd(*output_file_names)

    xml.write(XML_1_CONTENT)
    xml2.write(XML_2_CONTENT)

    cpp.write("""\
#include <stdint.h>
struct cppX
{
    IsarA defined_in_xml;
    IsarDefC defined_deeper_in_xmls;
    uint16_t regular_type;
    IsarDefA typedefed_deeper_in_xmls;
};
""")
    prophyc.main(["--sack", "--include_isar", str(xml2),
                  "--python_out", str(tmpdir_cwd), str(cpp)])

    assert all(map(os.path.isfile, map(str, output_files))), "Some files not created"

    assert xml_py.read() == """\
import prophy

IsarDefA = prophy.r32
IsarDefB = prophy.r32

class IsarDefC(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifC_a', prophy.u16),
                   ('ifC_b_len', prophy.u32),
                   ('ifC_b', prophy.array(prophy.u8, bound = 'ifC_b_len'))]
"""

    assert xml2_py.read() == """\
import prophy

from included_by_isar import *

class IsarA(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifA_a', prophy.u8),
                   ('ifA_B', IsarDefC)]

class IsarV(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('numOfItems', prophy.u32),
                   ('theItems', prophy.array(IsarDefB, bound = 'numOfItems'))]
"""

    assert cpp_py.read() == """\
import prophy

from included_by_sack import *

class cppX(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('defined_in_xml', IsarA),
                   ('defined_deeper_in_xmls', IsarDefC),
                   ('regular_type', prophy.u16),
                   ('typedefed_deeper_in_xmls', IsarDefA)]
"""


@pytest.mark.xfail(reason="isar supples not implemented in prophy parser")
def test_prophy_includes_isar(tmpdir_cwd, tmpfiles_cwd):

    input_file_names = ("included_by_isar.xml",
                        "included_by_prophy.xml",
                        "the.prophy")

    xml, xml2, the_prophy = tmpfiles_cwd(*input_file_names)

    xml.write(XML_1_CONTENT)
    xml2.write(XML_2_CONTENT)
    the_prophy.write("""

struct X
{
    IsarA defined_in_xml;
    IsarDefC defined_deeper_in_xmls;
    u16 regular_type;
    IsarDefA typedefed_deeper_in_xmls;
};
""")

    prophyc.main(["--include_isar", str(xml2),
                  "--python_out", str(tmpdir_cwd), str(the_prophy)])
