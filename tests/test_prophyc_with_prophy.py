import pytest
import os
import subprocess

main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
prophyc_dir = os.path.join(main_dir, "prophyc")
prophyc = os.path.join(prophyc_dir, "prophyc.py")

simple_isar = """<dom>
      <constant name="MAX_NUM_OF_L2DEPLOYABLE_NODE" value="10"/>
      <typedef name="TPoolId" type="u32"/>
      <typedef name="TNumberOfItems" primitiveType="32 bit integer unsigned"/>
      <enum name="EL2DeployableNode">
         <enum-member name="EL2DeployableNode_Basic1" value="0"/>
         <enum-member name="EL2DeployableNode_Basic2" value="1"/>
         <enum-member name="EL2DeployableNode_Basic3" value="2"/>
         <enum-member name="EL2DeployableNode_Basic4" value="3"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended1" value="10"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended2" value="11"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended3" value="12"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended4" value="13"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended5" value="14"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended6" value="15"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended7" value="16"/>
         <enum-member comment="(FDD only)" name="EL2DeployableNode_Extended8" value="17"/>
         <enum-member name="EL2DeployableNode_ArmL2Master" value="20"/>
         <enum-member name="EL2DeployableNode_ArmL2Slave" value="21"/>
         <enum-member name="EL2DeployableNode_DcmLrcPsMaster" value="22"/>
         <enum-member name="EL2DeployableNode_DcmLrcPsSlave" value="23"/>
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

def compile(filename, mode):
    cmd = " ".join(["python", prophyc, mode, "--python_out", ".", filename])
    subprocess.check_call(cmd, shell = True)

def compile_isar(filename):
    compile(filename, "--isar")

def compile_sack(filename):
    compile(filename, "--sack")

def write(filename, content):
    open(filename, "w").write(content)

def test_simple_struct(tmpdir_cwd):
    write("simple.xml", simple_isar)
    compile_isar("simple.xml")
    import simple

def test_simple_struct_construct(tmpdir_cwd):
    write("simple_construct.xml", simple_isar)
    compile_isar("simple_construct.xml")
    import simple_construct
    s = simple_construct.SL2DeploymentInfo()
    s.l2NodeType = "EL2DeployableNode_Basic2"
    s.nodeAddr = 0x1231
    assert "\x00\x00\x00\x01\x12\x31\x00\x00" == s.encode(">")

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
    write("protocol.hpp", content)
    compile_sack("protocol.hpp")

    import protocol
    x = protocol.X()
    x.a = 1
    x.b = 2
    x.c = 3

    assert "\x00\x00\x00\x01\x00\x02\x03\x00" == x.encode(">")
