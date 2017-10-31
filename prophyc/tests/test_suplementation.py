import pytest
import os

import prophyc

XML_1_CONTENT = """\
<x>
    <typedef name="IsarDefA" type="r32"/>
    <typedef name="IsarDefB" type="r64"/>
    <enum name="EIsarDefEnum">
        <enum-member name="EIsarDefEnum_A" value="0"/>
        <enum-member name="EIsarDefEnum_B" value="1"/>
        <enum-member name="EIsarDefEnum_C" value="2"/>
        <enum-member name="EIsarDefEnum_D" value="4"/>
    </enum>
    <constant name="IsarCONST_A" value="4"/>
    <constant name="IsarCONST_B" value="16"/>
    <struct name="IsarDefC">
        <member name="ifC_a" type="u16"/>
        <member name="ifC_b" type="u64">
            <dimension isVariableSize="true"/>
        </member>
    </struct>
</x>
"""

XML_2_CONTENT = """\
<x>
    <include href="isar_root_defs.xml"/>
    <struct name="IsarK">
        <member name="ifK_a" type="u8"/>
        <member name="ifK_B" type="IsarDefB">
            <dimension size="IsarCONST_A"/>
        </member>
    </struct>
    <struct name="IsarL">
        <member name="theBItems" type="IsarDefB">
            <dimension isVariableSize="true" variableSizeFieldName="numOfItems"/>
        </member>
    </struct>
</x>
"""

XML_3_CONTENT = """\
<x>
    <include href="isar_root_defs.xml"/>
    <struct name="IsarV">
        <member name="ifV_a" type="IsarDefA"/>
        <member name="ifV_b" type="IsarDefB">
            <dimension isVariableSize="true" size="IsarCONST_B"/>
        </member>
        <member name="ifV_c" type="EIsarDefEnum"/>
    </struct>
</x>
"""

@pytest.clang_installed
def test_sack_includes_isar(tmpdir_cwd, tmpfiles_cwd):

    input_file_names = ("isar_root_defs.xml",
                        "included_by_sack_a.xml",
                        "included_by_sack_b.xml",
                        "the_sack.cpp")

    xml1, xml2, xml3, cpp = tmpfiles_cwd(*input_file_names)

    output_file_names = map(lambda f: os.path.splitext(f)[0] + '.py', input_file_names)
    xml_py, xml2_py, xml3_py, cpp_py = output_files = tmpfiles_cwd(*output_file_names)

    xml1.write(XML_1_CONTENT)
    xml2.write(XML_2_CONTENT)
    xml3.write(XML_3_CONTENT)

    cpp.write("""\
#include <stdint.h>
struct cppX
{
    IsarK defined_in_xml;
    IsarDefC defined_deeper_in_xmls;
    uint16_t regular_type;
    IsarDefA typedefed_deeper_in_xmls;
};
""")
    prophyc.main(["--sack", "--include_isar", str(xml2), "--include_isar", str(xml3),
                  "--python_out", str(tmpdir_cwd), str(cpp)])

    assert all(map(os.path.isfile, map(str, output_files))), "Some files not created"

    assert xml_py.read() == """\
import prophy

IsarCONST_A = 4
IsarCONST_B = 16

IsarDefA = prophy.r32
IsarDefB = prophy.r64

class EIsarDefEnum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators  = [('EIsarDefEnum_A', 0),
                     ('EIsarDefEnum_B', 1),
                     ('EIsarDefEnum_C', 2),
                     ('EIsarDefEnum_D', 4)]

EIsarDefEnum_A = 0
EIsarDefEnum_B = 1
EIsarDefEnum_C = 2
EIsarDefEnum_D = 4

class IsarDefC(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifC_a', prophy.u16),
                   ('ifC_b_len', prophy.u32),
                   ('ifC_b', prophy.array(prophy.u64, bound = 'ifC_b_len'))]
"""

    assert xml2_py.read() == """\
import prophy

from isar_root_defs import *

class IsarK(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifK_a', prophy.u8),
                   ('ifK_B', prophy.array(IsarDefB, size = IsarCONST_A))]

class IsarL(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('numOfItems', prophy.u32),
                   ('theBItems', prophy.array(IsarDefB, bound = 'numOfItems'))]
"""

    assert xml3_py.read() == """\
import prophy

from isar_root_defs import *

class IsarV(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifV_a', IsarDefA),
                   ('ifV_b_len', prophy.u32),
                   ('ifV_b', prophy.array(IsarDefB, bound = 'ifV_b_len', size = IsarCONST_B)),
                   ('ifV_c', EIsarDefEnum)]
"""

    assert cpp_py.read() == """\
import prophy

from included_by_sack_a import *
from included_by_sack_b import *

class cppX(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('defined_in_xml', IsarK),
                   ('defined_deeper_in_xmls', IsarDefC),
                   ('regular_type', prophy.u16),
                   ('typedefed_deeper_in_xmls', IsarDefA)]
"""
