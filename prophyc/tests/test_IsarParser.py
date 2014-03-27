# -*- coding: utf-8 -*-

import DataHolder
import IsarParser
import PythonSerializer
from collections import namedtuple

def parse(xml_string):
    return IsarParser.IsarParser().parse_string(xml_string)

def test_includes_parsing():
    xml = """\
<system xmlns:xi="http://www.nsn.com/2008/XInclude">
    <xi:include href="mydlo.xml"/>
    <xi:include href="szydlo.xml"/>
    <xi:include href="powidlo.xml"/>
</system>
"""
    holder = parse(xml)

    assert ["mydlo", "szydlo", "powidlo"] == holder.includes

def test_typedefs_primitive_type_parsing():
    xml = """\
<x>
    <typedef name="a" primitiveType="8 bit integer unsigned"/>
    <typedef name="b" primitiveType="16 bit integer unsigned"/>
    <typedef name="c" primitiveType="32 bit integer unsigned"/>
    <typedef name="d" primitiveType="64 bit integer unsigned"/>
    <typedef name="e" primitiveType="8 bit integer signed"/>
    <typedef name="f" primitiveType="16 bit integer signed"/>
    <typedef name="g" primitiveType="32 bit integer signed"/>
    <typedef name="h" primitiveType="64 bit integer signed"/>
    <typedef name="i" primitiveType="32 bit float"/>
    <typedef name="j" primitiveType="64 bit float"/>
</x>
"""
    holder = parse(xml)

    assert [("a", "u8"),
            ("b", "u16"),
            ("c", "u32"),
            ("d", "u64"),
            ("e", "i8"),
            ("f", "i16"),
            ("g", "i32"),
            ("h", "i64"),
            ("i", "r32"),
            ("j", "r64")] == holder.typedefs

def test_typedefs_parsing():
    xml = """<typedef name="TILoveTypedefs_ALot" type="MyType"/>"""
    holder = parse(xml)

    assert [("TILoveTypedefs_ALot", "MyType")] == holder.typedefs

def test_enums_parsing():
    xml = """\
<enum name="EEnum">
    <enum-member name="EEnum_A" value="0"/>
    <enum-member name="EEnum_B" value="1"/>
    <enum-member name="EEnum_C" value="-1"/>
</enum>
"""
    holder = parse(xml)

    assert 1 == len(holder.enums)
    assert "EEnum" == holder.enums[0][0]
    assert [("EEnum_A", "0"), ("EEnum_B", "1"), (u"EEnum_C", "0xFFFFFFFF")] == holder.enums[0][1]

def test_constants_parsing():
    xml = """\
<x>
    <constant name="CONST_A" value="0"/>
    <constant name="CONST_B" value="31"/>
</x>
"""
    holder = parse(xml)

    assert [("CONST_A", "0"), ("CONST_B", "31")] == holder.constants

def test_constants_parsing_and_sorting():
    xml = """\
<x>
    <constant name="C_A" value="C_B + C_C"/>
    <constant name="C_B" value="1"/>
    <constant name="C_C" value="2"/>
</x>
"""
    holder = parse(xml)

    assert [("C_B", "1"), ("C_C", "2"), ("C_A", "C_B + C_C")] == holder.constants

def test_struct_parsing():
    xml = """\
<struct name="Struct">
    <member name="a" type="u8"/>
    <member name="b" type="i64"/>
    <member name="c" type="r32"/>
    <member name="d" type="TTypeX"/>
</struct>
"""
    holder = parse(xml)

    assert 1 == len(holder.struct_list)
    assert 4 == len(holder.struct_list[0].list)
    assert "Struct" == holder.struct_list[0].name
    assert "a" == holder.struct_list[0].list[0].name
    assert "u8" == holder.struct_list[0].list[0].type
    assert "b" == holder.struct_list[0].list[1].name
    assert "i64" == holder.struct_list[0].list[1].type
    assert "c" == holder.struct_list[0].list[2].name
    assert "r32" == holder.struct_list[0].list[2].type
    assert "d" == holder.struct_list[0].list[3].name
    assert "TTypeX" == holder.struct_list[0].list[3].type

# """ FIXME kl. don't test PythonSerializer together with IsarParser """
#
# def test_of_error_in_SPuschReceiveReq():
#     xml = ('<struct comment="" name="SPuschReceiveReq">\n'
#            '   <member comment="" name="cqiRespDBuffer" type="SPhyDataBuffer"/>\n'
#            '   <member comment="" name="measRespBuffer" type="SPhyDataBuffer"/>\n'
#            '   <member comment="" name="measRespBuffer2" type="SPhyDataBuffer"/>\n'
#            '   <member comment="" name="cellMeasRespBuffer" type="SPhyDataBuffer"/>\n'
#            '   <member comment="" name="rfLoopFlag" type="TBoolean"/>\n'
#            '   <member comment="" name="numOfDelayedUe" rangeDescription="0..MAX_PUSCH_UES_PER_TTI_5MHZ, 0..MAX_PUSCH_UES_PER_TTI_10MHZ, 0..MAX_PUSCH_UES_PER_TTI_15MHZ, 0..MAX_PUSCH_UES_PER_TTI_20MHZ" type="TNumberOfItems"/>\n'
#            '   <member comment="" maxRange="MAX_UINT16" minRange="0" name="delayedUe" type="TCrntiU16">\n'
#            '      <dimension minSize="1" size="MAX_PUSCH_UES_PER_TTI_20MHZ"/>\n'
#            '   </member>\n'
#            '   <member comment="" name="numOfSCellAddressingInfo" rangeDescription="For FSMr3: 0 MAX_NUM_SCELLS; For FSMr2: 0." type="TNumberOfItems"/>\n'
#            '   <member comment="" maxRange="MAX_NUM_OF_PUSCH_RECEIVE_REQ" minRange="0" name="numOfUePuschReq" type="TNumberOfItems"/>\n'
#            '   <member name="uePuschReq" type="SPuschUeReceiveReq">\n'
#            '      <dimension size="THIS_IS_VARIABLE_SIZE_ARRAY"/>\n'
#            '   </member>\n'
#            '</struct>\n')
#
#     dh = IsarParser.IsarParser().parse_string(xml)
#     ps = PythonSerializer.PythonSerializer()
#     """ FIXME kl. how does serialize relate to _serialize_msgs? These methods seem to do the same, but
#     first one generates really weird formatting with abundance of newlines"""
#     output = ps.serialize_string(dh)
#
#     assert ("import prophy\n"
#             "\n"
#             "class SPuschReceiveReq(prophy.struct):\n"
#             "    __metaclass__ = prophy.struct_generator\n"
#             "    _descriptor = [('cqiRespDBuffer',SPhyDataBuffer), ('measRespBuffer',SPhyDataBuffer), ('measRespBuffer2',SPhyDataBuffer), ('cellMeasRespBuffer',SPhyDataBuffer), ('rfLoopFlag',TBoolean), ('numOfDelayedUe',TNumberOfItems), ('tmpName',TNumberOfItems), ('delayedUe',prophy.array(TCrntiU16,bound='tmpName')), ('numOfSCellAddressingInfo',TNumberOfItems), ('numOfUePuschReq',TNumberOfItems), ('uePuschReq',prophy.bytes(size=THIS_IS_VARIABLE_SIZE_ARRAY))]\n") == output
#
# def test_of_backward_compatibility_serialization():
#     xml = ('<struct comment="cmt0" name="SPuschUeReceiveMeasResp">\n'
#            '    <member comment="cmt1" maxRange="MAX_UINT16" minRange="0" name="crnti" type="TCrntiU16"/>\n'
#            '    <member comment="cmt2" name="ueIndex" type="TUeIndex"/>\n'
#            '    <member comment="cmt3" maxRange="EStatusLte_NotOk" minRange="EStatusLte_Ok" name="status" type="EStatusLte"/>\n'
#            '    <member comment="cmt4" name="specificCause" type="ESpecificCauseLte"/>\n'
#            '    <member comment="cmt5" name="rssi" type="TRssi"/>\n'
#            '    <member comment="cmt6" name="interferencePower" type="TInterferencePower"/>\n'
#            '    <member comment="cmt7" name="frequencyOffsetPusch" type="TFrequencyOffset"/>\n'
#            '    <member comment="cmt8" name="phiReal" type="TTimeEstPhi"/>\n'
#            '    <member comment="cmt9" name="phiImag" type="TTimeEstPhi"/>\n'
#            '    <member comment="cmt10" maxRange="400" minRange="-200" name="postCombSinr" type="i16"/>\n'
#            '    <member comment="cmt11" name="ulCompUsage" rangeDescription="0...1" type="u8"/>\n'
#            '    <member comment="cmt12" name="ulReliabilty" type="TBooleanU8"/>\n'
#            '    <member comment="cmt13" defaultValue="0" name="subCellId" type="TSubCellIdU8"/>\n'
#            '    <member name="explicitPadding1" type="u8"/>\n'
#            '    <member name="explicitPadding2" type="u16"/>\n'
#            '</struct>')
#
#     dh = IsarParser.IsarParser().parse_string(xml)
#     ps = PythonSerializer.PythonSerializer()
#     output = ps._serialize_msgs(dh.struct_list)
#
#     assert ("class SPuschUeReceiveMeasResp(prophy.struct):\n"
#             "    __metaclass__ = prophy.struct_generator\n"
#             "    _descriptor = [('crnti',TCrntiU16), ('ueIndex',TUeIndex), ('status',EStatusLte), ('specificCause',ESpecificCauseLte), ('rssi',TRssi), ('interferencePower',TInterferencePower), ('frequencyOffsetPusch',TFrequencyOffset), ('phiReal',TTimeEstPhi), ('phiImag',TTimeEstPhi), ('postCombSinr',prophy.i16), ('ulCompUsage',prophy.u8), ('ulReliabilty',TBooleanU8), ('subCellId',TSubCellIdU8), ('explicitPadding1',prophy.u8), ('explicitPadding2',prophy.u16)]\n") == output
