from collections import namedtuple
from contextlib import contextmanager
import os
import pytest


IsarTestItem = namedtuple("IsarTestItem", "file_name_base, input_xml, expected_py")

ISAR_TEST_SET_1 = [

    IsarTestItem(
        file_name_base="isar_root_defs",
        input_xml="""\
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
""",
        expected_py="""\
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
"""),


    IsarTestItem(
        file_name_base="included_by_sack_a",
        input_xml="""\
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
""",
        expected_py="""\
import prophy

from isar_root_defs import *

class IsarK(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifK_a', prophy.u8),
                   ('ifK_B', prophy.array(IsarDefB, size = IsarCONST_A))]

class IsarL(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('numOfItems', prophy.u32),
                   ('theBItems', prophy.array(IsarDefB, bound = 'numOfItems'))]
"""),

    IsarTestItem(
        file_name_base="included_by_sack_b",
        input_xml="""\
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
""",
        expected_py="""\
import prophy

from isar_root_defs import *

class IsarV(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('ifV_a', IsarDefA),
                   ('ifV_b_len', prophy.u32),
                   ('ifV_b', prophy.array(IsarDefB, bound = 'ifV_b_len', size = IsarCONST_B)),
                   ('ifV_c', EIsarDefEnum)]
""")
]


@pytest.fixture
def isar_test_helper(tmpdir_cwd):
    @contextmanager
    def check_isars_generated(isar_test_set):
        names, xml_contents, expected_py_contents = zip(*isar_test_set)
        xmls, pys = zip(*map(lambda b: (tmpdir_cwd.join(b + '.xml'), tmpdir_cwd.join(b + '.py')), names))
        list(map(lambda t: t[0].write(t[1]), zip(xmls, xml_contents)))

        yield xmls

        for py_file, py_content in zip(pys, expected_py_contents):
            assert os.path.isfile(str(py_file)), "The PY file {} doesn't exist.".format(py_file)
            assert py_file.read() == py_content

    return check_isars_generated


@pytest.clang_installed
def test_sack_supples(isar_test_helper, tmpdir_cwd, call_prophyc):
    cpp = tmpdir_cwd.join('the_sack.hpp')
    cppy = tmpdir_cwd.join('the_sack.py')
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

    with isar_test_helper(ISAR_TEST_SET_1) as (_, xml2, xml3):
        args = ["--sack", "--include_isar", str(xml2), "--include_isar", str(xml3),
                "--python_out", str(tmpdir_cwd), str(cpp)]
        ret, out, err = call_prophyc(args)
        assert out == ""
        assert err == ""
        assert ret == 0
    assert cppy.read() == """\
import prophy

from included_by_sack_a import *
from included_by_sack_b import *

class cppX(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('defined_in_xml', IsarK),
                   ('defined_deeper_in_xmls', IsarDefC),
                   ('regular_type', prophy.u16),
                   ('typedefed_deeper_in_xmls', IsarDefA)]
"""


@pytest.clang_installed
def test_sack_supples_array_size_from_isar(isar_test_helper, tmpdir_cwd, call_prophyc):
    cpp = tmpdir_cwd.join('the_sack.hpp')
    cppy = tmpdir_cwd.join('the_sack.py')
    cpp.write("""\
#include <stdint.h>
struct cppX
{
    IsarV type_from_isar[IsarCONST_A];
    uint16_t regular_type[IsarCONST_B];
};
""")

    with isar_test_helper(ISAR_TEST_SET_1) as (_, xml2, xml3):
        args = ["--sack", "--include_isar", str(xml2), "--include_isar", str(xml3),
                "--python_out", str(tmpdir_cwd), str(cpp)]
        ret, out, err = call_prophyc(args)
        assert out == ""
        assert err == ""
        assert ret == 0
    assert cppy.read() == """\
import prophy

from included_by_sack_a import *
from included_by_sack_b import *

class cppX(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('type_from_isar', prophy.array(IsarV, size = 4)),
                   ('regular_type', prophy.array(prophy.u16, size = 16))]
"""


@pytest.clang_installed
def test_sack_supples_static_consts_values_from_isar(isar_test_helper, tmpdir_cwd, call_prophyc):
    cpp = tmpdir_cwd.join('the_sack.hpp')
    cppy = tmpdir_cwd.join('the_sack.py')
    cpp.write("""\
#include <stdint.h>
struct constants
{
    static const uint16_t A = IsarCONST_A;
    static const uint16_t B = IsarCONST_B;
    static const uint16_t C = A + B;
};

struct cppX
{
    uint8_t straigth[2];
    uint16_t tricky1[constants::A];
    uint16_t tricky2[constants::C];
    uint16_t tricky3[constants::A * constants::B];
};
""")

    with isar_test_helper(ISAR_TEST_SET_1) as (_, xml2, xml3):
        args = ["--sack", "--include_isar", str(xml2), "--include_isar", str(xml3),
                "--python_out", str(tmpdir_cwd), str(cpp)]
        ret, out, err = call_prophyc(args)
        assert out == ""
        assert err == ""
        assert ret == 0

    assert cppy.read() == """\
import prophy

from included_by_sack_a import *
from included_by_sack_b import *

class constants(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = []

class cppX(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [('straigth', prophy.array(prophy.u8, size = 2)),
                   ('tricky1', prophy.array(prophy.u16, size = 4)),
                   ('tricky2', prophy.array(prophy.u16, size = 20)),
                   ('tricky3', prophy.array(prophy.u16, size = 64))]
"""

@pytest.clang_installed
def test_warns_with_supplementation(isar_test_helper, tmpdir_cwd, call_prophyc):
    cpp = tmpdir_cwd.join('the_sack.hpp')
    cpp.write("""\
#include <stdint.h>
struct cppX
{
    static const int8_t A = 256 * IsarCONST_A;
    uint8_t straigth[2];
};
""")

    with isar_test_helper(ISAR_TEST_SET_1) as (_, xml2, xml3):
        args = ["--sack", "--include_isar", str(xml2), "--include_isar", str(xml3),
                "--python_out", str(tmpdir_cwd), str(cpp)]
        ret, out, err = call_prophyc(args)
        assert out == ""
        assert "the_sack.hpp:4:33: warning: implicit conversion from 'int' to 'const int8_t'" in err
        assert ret == 0
