import pytest
import os
import subprocess

main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
prophyc_dir = os.path.join(main_dir, "prophyc")
prophyc = os.path.join(prophyc_dir, "prophyc.py")

simple_isar = """<dom>
      <typedef name="TPoolId" type="u32"/>
          <include name="TNumberOfItems.h">
      <typedef name="TNumberOfItems" primitiveType="32 bit integer unsigned"/>
      </include>
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

complex_isar = """<dom>
      <typedef name="u32" type="prophy.u32"/>
      <struct name="S">
         <member name="l2NodeType" type="S1"/>
            <dimension isVariableSize="true" size="MAX_NUM_OF_L2DEPLOYABLE_NODE" variableSizeFieldName="numOfDeploymentInfo" variableSizeFieldType="u32"/>
         <member name="blabla" type="u32"/>
      </struct>
      <struct name="x">
         <member name="poolId" type="u32"/>
         <member name="deploymentInfo" type="S">
            <dimension isVariableSize="true" size="MAX_NUM_OF_L2DEPLOYABLE_NODE" variableSizeFieldName="numOfDeploymentInfo" variableSizeFieldType="u32"/>
         </member>
      </struct>
      
      <struct name="S1">
         <member name="l2NodeType" type="u32"/>
         <member name="blabla" type="u32"/>
      </struct>
     </dom>
"""

to_sort = """<dom>
      <typedef name="u32" type="prophy.u32"/>
      <struct name="S">
         <member name="l2NodeType" type="S1"/>
            <dimension isVariableSize="true" size="MAX_NUM_OF_L2DEPLOYABLE_NODE" variableSizeFieldName="numOfDeploymentInfo" variableSizeFieldType="u32"/>
         <member name="blabla" type="u32"/>
      </struct>
      <struct name="x">
         <member name="poolId" type="u32"/>
         <member name="deploymentInfo" type="S">
            <dimension isVariableSize="true" size="MAX_NUM_OF_L2DEPLOYABLE_NODE" variableSizeFieldName="numOfDeploymentInfo" variableSizeFieldType="u32"/>
         </member>
      </struct>
      
      <struct name="S1">
         <member name="l2NodeType" type="u32"/>
         <member name="blabla" type="u32"/>
      </struct>
     </dom>
"""

def compile(filename):
    cmd = " ".join(["python", prophyc, "--isar", "--python_out", ".", filename])
    subprocess.check_call(cmd, shell = True)

def write(filename, content):
    open(filename, "w").write(simple_isar)

def test_simple_struct(tmpdir_cwd):
    write("simple.xml", simple_isar)
    compile("simple.xml")
    import simple

def test_simple_struct_construct(tmpdir_cwd):
    write("simple_construct.xml", simple_isar)
    compile("simple_construct.xml")
    import simple_construct
    s = simple_construct.SL2DeploymentInfo()
    s.l2NodeType = "EL2DeployableNode_Basic2"
    print s.l2NodeType

def test_complex_struct(tmpdir_cwd):
    write("complex.xml", complex_isar)
    compile("complex.xml")
    import complex

def test_struct_sort(tmpdir_cwd):
    write("sort.xml", to_sort)
    compile("sort.xml")
    import sort
