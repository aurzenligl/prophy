import os
import sys
import subprocess
import pytest

opd = os.path.dirname
opr = os.path.realpath
main_dir = opd(opd(opr(__file__)))

def write(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def compile(filename, mode, tmpdir):
    cmd = " ".join([sys.executable, "-m", "prophyc", mode, "--python_out",
                    tmpdir, os.path.join(tmpdir, filename)])
    subprocess.check_call(cmd, cwd = main_dir, shell = True)

def test_isar_input(tmpdir_cwd):
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
        <member comment="Pool ID&#13;&#10;In a non Super Pool configuration can be set to 0." name="poolId" type="TPoolId"/>
        <member comment="NID for each deployable node type." name="deploymentInfo" type="SL2DeploymentInfo">
            <dimension isVariableSize="true" minSize="1" size="MAX_NUM_OF_L2DEPLOYABLE_NODE" variableSizeFieldComment="Currently either 4 or 8" variableSizeFieldName="numOfDeploymentInfo"/>
        </member>
    </struct>
    <struct name="SL2DeploymentInfo">
        <member comment="Deployable node type" name="l2NodeType" type="EL2DeployableNode"/>
        <member comment="NID" name="nodeAddr" type="TAaSysComNid"/>
    </struct>
</dom>
"""

    write("isar.xml", content)
    compile("isar.xml", mode = '--isar', tmpdir = str(tmpdir_cwd))

    import isar
    s = isar.SL2DeploymentInfo()
    s.l2NodeType = "EL2DeployableNode_Basic2"
    s.nodeAddr = 0x1231

    assert b"\x00\x00\x00\x01\x12\x31\x00\x00" == s.encode(">")

@pytest.clang_installed
def test_sack_input(tmpdir_cwd):
    content = """\
#include <stdint.h>
struct X
{
    uint32_t a;
    uint16_t b;
    uint8_t c;
};
"""

    write("sack.hpp", content)
    compile("sack.hpp", mode = '--sack', tmpdir = str(tmpdir_cwd))

    import sack
    x = sack.X()
    x.a = 1
    x.b = 2
    x.c = 3

    assert b"\x00\x00\x00\x01\x00\x02\x03\x00" == x.encode(">")
