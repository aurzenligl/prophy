import os
import pytest

opd = os.path.dirname
opr = os.path.realpath
main_dir = opd(opd(opr(__file__)))

def form_args(mode, tmpdir_cwd, target_file_name):
    return [mode, "--python_out", str(tmpdir_cwd), os.path.join(str(tmpdir_cwd), target_file_name)]

def test_isar_input(tmpdir_cwd, call_prophyc):
    content = """\
<dom>
    <constant name="MAX_NUM_OF_L2DEPLOYABLE_NODE" value="10"/>
    <typedef name="TPoolId" type="u32"/>
    <typedef name="TNumberOfItems" primitiveType="32 bit integer unsigned"/>
    <enum name="EL2DeployableNode">
        <enum-member name="EL2DeployableNode_Basic1" value="0"/>
        <enum-member name="EL2DeployableNode_Basic2" value="1"/>
        <enum-member name="EL2DeployableNode_Basic3" value="2"/>
        <enum-member name="EL2DeployableNode_Basic4" value="3"/>
    </enum>
    <typedef name="TAaSysComNid" primitiveType="16 bit integer unsigned"/>
    <struct name="SL2PoolInfo">
        <member comment="Pool ID&#13;&#10;In a non Super Pool configuration can be set to 0." name="poolId" \
        type="TPoolId"/>
        <member comment="NID for each deployable node type." name="deploymentInfo" type="SL2DeploymentInfo">
            <dimension isVariableSize="true" minSize="1" size="MAX_NUM_OF_L2DEPLOYABLE_NODE" \
            variableSizeFieldComment="Currently either 4 or 8" variableSizeFieldName="numOfDeploymentInfo"/>
        </member>
    </struct>
    <struct name="SL2DeploymentInfo">
        <member comment="Deployable node type" name="l2NodeType" type="EL2DeployableNode"/>
        <member comment="NID" name="nodeAddr" type="TAaSysComNid"/>
    </struct>
</dom>
"""

    xml_file_name = "isar.xml"
    tmpdir_cwd.join(xml_file_name).write(content)

    call_prophyc(form_args("--isar", tmpdir_cwd, xml_file_name))

    import isar
    s = isar.SL2DeploymentInfo()
    s.l2NodeType = "EL2DeployableNode_Basic2"
    s.nodeAddr = 0x1231

    assert b"\x00\x00\x00\x01\x12\x31\x00\x00" == s.encode(">")

@pytest.clang_installed
def test_sack_input(tmpdir_cwd, call_prophyc):
    content = """\
#include <stdint.h>
struct X
{
    uint32_t a;
    uint16_t b;
    uint8_t c;
};
"""

    sack_file_name = "sack.hpp"
    tmpdir_cwd.join(sack_file_name).write(content)
    call_prophyc(form_args("--sack", tmpdir_cwd, sack_file_name))

    import sack
    x = sack.X()
    x.a = 1
    x.b = 2
    x.c = 3

    assert b"\x00\x00\x00\x01\x00\x02\x03\x00" == x.encode(">")
